#!/usr/bin/env python3
"""問題データ（JSON マスター）の自動検査スクリプト。

検査内容
  1. JSON 構文（エラー行・列を表示）
  2. schemas/question_schema.json によるスキーマ検証
  3. 必須フィールド（ID・正答・解説・難易度 など）の欠落・空値
  4. 整合性（ID 重複、単元 ID の存在、選択肢と正答の対応、配点合計、参照切れ 等）
  5. 問題文の重複・過度な類似（正規化テキストのハッシュ＋文字 3-gram の Jaccard 類似度）
  6. 検算補助（calc_check の式を sympy で安全に評価して期待値と照合）

使い方
  python scripts/validate_questions.py                 # data/ 以下の全 JSON を検査
  python scripts/validate_questions.py data/pilot      # ディレクトリ・ファイルを指定
  python scripts/validate_questions.py --strict        # 警告もエラー扱い
  python scripts/validate_questions.py --stamp         # 検査結果を各 JSON の validation に記録
  python scripts/validate_questions.py --report out.json

終了コード: 0 = 合格, 1 = エラーあり（--strict 時は警告も含む）, 2 = 実行時エラー
"""
from __future__ import annotations

import argparse
import ast
import bisect
import datetime as _dt
import hashlib
import json
import re
import signal
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

VALIDATOR_VERSION = "1.0.0"
ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schemas" / "question_schema.json"
CURRICULUM_PATH = ROOT / "schemas" / "curriculum_map.json"
DEFAULT_DATA_DIR = ROOT / "data"

# --------------------------------------------------------------------------
# 結果の入れ物
# --------------------------------------------------------------------------


@dataclass
class Issue:
    level: str  # "ERROR" | "WARNING"
    file: str
    line: int | None
    category: str
    path: str
    message: str

    def format(self) -> str:
        loc = f"{self.file}:{self.line}" if self.line else self.file
        p = f" {self.path}:" if self.path else ""
        return f"{loc}: {self.level} [{self.category}]{p} {self.message}"


@dataclass
class FileResult:
    path: Path
    rel: str
    data: Any = None
    positions: dict = field(default_factory=dict)
    issues: list = field(default_factory=list)

    @property
    def errors(self) -> int:
        return sum(1 for i in self.issues if i.level == "ERROR")

    @property
    def warnings(self) -> int:
        return sum(1 for i in self.issues if i.level == "WARNING")


class Reporter:
    def __init__(self) -> None:
        self.files: list[FileResult] = []
        self.global_issues: list[Issue] = []

    def add(self, fr: FileResult, level: str, category: str, path: tuple | str, message: str) -> None:
        path_t = path if isinstance(path, tuple) else ()
        path_s = path if isinstance(path, str) else format_path(path_t)
        fr.issues.append(Issue(level, fr.rel, line_for(fr.positions, path_t), category, path_s, message))

    @property
    def all_issues(self) -> list[Issue]:
        out = []
        for f in self.files:
            out.extend(f.issues)
        return out


# --------------------------------------------------------------------------
# JSON の行番号対応（JSON パス → 行番号）
# --------------------------------------------------------------------------


class _PosParser:
    """標準 json で読めたテキストを再走査し、各値の開始行を記録する最小パーサ。"""

    _ws = re.compile(r"[ \t\r\n]*")
    _num = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?")

    def __init__(self, text: str) -> None:
        self.s = text
        self.line_starts = [0] + [m.end() for m in re.finditer("\n", text)]
        self.pos: dict[tuple, int] = {}

    def line(self, idx: int) -> int:
        return bisect.bisect_right(self.line_starts, idx)

    def skip(self, i: int) -> int:
        return self._ws.match(self.s, i).end()

    def parse(self) -> dict[tuple, int]:
        self.value(self.skip(0), ())
        return self.pos

    def value(self, i: int, path: tuple) -> int:
        self.pos[path] = self.line(i)
        c = self.s[i]
        if c == "{":
            i = self.skip(i + 1)
            if self.s[i] == "}":
                return i + 1
            while True:
                key_start = i
                key, i = self.string(i)
                self.pos[path + (key,)] = self.line(key_start)
                i = self.skip(i)
                i = self.skip(i + 1)  # ':'
                i = self.value(i, path + (key,))
                # value() は自身の開始行で上書きするので、キー行を優先して戻す
                self.pos[path + (key,)] = self.line(key_start)
                i = self.skip(i)
                if self.s[i] == ",":
                    i = self.skip(i + 1)
                    continue
                return i + 1
        if c == "[":
            i = self.skip(i + 1)
            if self.s[i] == "]":
                return i + 1
            k = 0
            while True:
                i = self.value(i, path + (k,))
                k += 1
                i = self.skip(i)
                if self.s[i] == ",":
                    i = self.skip(i + 1)
                    continue
                return i + 1
        if c == '"':
            return self.string(i)[1]
        m = self._num.match(self.s, i)
        if m and m.end() > i:
            return m.end()
        for lit in ("true", "false", "null"):
            if self.s.startswith(lit, i):
                return i + len(lit)
        raise ValueError(f"unexpected character at {i}")

    def string(self, i: int) -> tuple[str, int]:
        val, end = json.decoder.scanstring(self.s, i + 1)
        return val, end


def line_for(positions: dict, path: tuple) -> int | None:
    p = tuple(path)
    while True:
        if p in positions:
            return positions[p]
        if not p:
            return None
        p = p[:-1]


def format_path(path: Iterable) -> str:
    out = ""
    for p in path:
        out += f"[{p}]" if isinstance(p, int) else (f".{p}" if out else str(p))
    return out


# --------------------------------------------------------------------------
# 検算補助（sympy による安全な式評価）
# --------------------------------------------------------------------------

class CalcError(Exception):
    pass


def _build_env():
    import sympy as sp

    def perm(n, r):
        return sp.factorial(n) / sp.factorial(n - r)

    def mean(xs):
        xs = list(xs)
        return sp.Add(*xs) / len(xs)

    def median(xs):
        xs = sorted(xs)
        n = len(xs)
        return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2

    def variance(xs):
        xs = list(xs)
        m = mean(xs)
        return sp.Add(*[(x - m) ** 2 for x in xs]) / len(xs)

    def quartiles(xs):
        """中学校数学の方法（中央値で前半・後半に分け、各中央値をとる）。"""
        xs = sorted(xs)
        n = len(xs)
        lower, upper = xs[: n // 2], xs[(n + 1) // 2:]
        return [median(lower), median(xs), median(upper)]

    def deg(x):
        return x * sp.pi / 180

    funcs = {
        "sqrt": sp.sqrt, "root": sp.root, "Rational": sp.Rational, "expand": sp.expand,
        "factor": sp.factor, "simplify": sp.simplify, "solve": sp.solve, "Eq": sp.Eq,
        "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "asin": sp.asin, "acos": sp.acos,
        "atan": sp.atan, "log": sp.log, "exp": sp.exp, "Abs": sp.Abs, "diff": sp.diff,
        "integrate": sp.integrate, "limit": sp.limit, "summation": sp.summation,
        "binomial": sp.binomial, "comb": sp.binomial, "perm": perm, "factorial": sp.factorial,
        "gcd": sp.gcd, "lcm": sp.lcm, "nsimplify": sp.nsimplify, "floor": sp.floor,
        "ceiling": sp.ceiling, "Min": sp.Min, "Max": sp.Max, "re": sp.re, "im": sp.im,
        "conjugate": sp.conjugate, "isprime": sp.isprime, "divisors": sp.divisors,
        "factorint": sp.factorint, "mean": mean, "median": median, "variance": variance,
        "std": lambda xs: sp.sqrt(variance(xs)), "quartiles": quartiles, "deg": deg,
        "sorted": sorted, "len": len, "sum": lambda xs: sp.Add(*list(xs)), "N": sp.N,
        "collect": sp.collect, "cancel": sp.cancel, "apart": sp.apart, "together": sp.together,
        "trigsimp": sp.trigsimp, "radsimp": sp.radsimp, "Mod": sp.Mod, "range": lambda *a: list(range(*[int(x) for x in a])),
        "Matrix": sp.Matrix, "solveset": sp.solveset, "Interval": sp.Interval, "S": sp.S,
        "reduce_inequalities": sp.reduce_inequalities, "Lt": sp.Lt, "Le": sp.Le, "Gt": sp.Gt, "Ge": sp.Ge,
        "nroots": sp.nroots, "Symbol": None,
    }
    funcs.pop("Symbol")
    consts = {"pi": sp.pi, "E": sp.E, "I": sp.I, "oo": sp.oo}
    symbols = {n: sp.Symbol(n) for n in "a b c d h k m n p q r s t u v w x y z".split()}
    symbols["theta"] = sp.Symbol("theta")
    return sp, funcs, consts, symbols


_ENV = None


def safe_eval(expr: str):
    """許可されたノード・関数のみを評価する（eval は使わない）。"""
    global _ENV
    if _ENV is None:
        _ENV = _build_env()
    sp, funcs, consts, symbols = _ENV
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise CalcError(f"式の構文エラー: {e.msg}") from None

    binops = {
        ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b, ast.Mult: lambda a, b: a * b,
        ast.Div: lambda a, b: sp.sympify(a) / sp.sympify(b), ast.Pow: lambda a, b: sp.sympify(a) ** b,
        ast.Mod: lambda a, b: sp.Mod(a, b), ast.FloorDiv: lambda a, b: sp.floor(sp.sympify(a) / b),
    }

    def ev(node):
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant):
            v = node.value
            if isinstance(v, bool) or v is None:
                raise CalcError("真偽値・None は使えません")
            if isinstance(v, int):
                return sp.Integer(v)
            if isinstance(v, float):
                return sp.Rational(repr(v))
            if isinstance(v, str) and len(v) <= 200:
                return v
            raise CalcError("許可されていない定数です")
        if isinstance(node, ast.Name):
            if node.id in symbols:
                return symbols[node.id]
            if node.id in consts:
                return consts[node.id]
            raise CalcError(f"未定義の名前: {node.id}")
        if isinstance(node, ast.BinOp) and type(node.op) in binops:
            return binops[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            v = ev(node.operand)
            return -v if isinstance(node.op, ast.USub) else v
        if isinstance(node, (ast.List, ast.Tuple)):
            return [ev(e) for e in node.elts]
        if isinstance(node, ast.Set):
            return sp.FiniteSet(*[ev(e) for e in node.elts])
        if isinstance(node, ast.Dict):
            return {ev(k): ev(v) for k, v in zip(node.keys, node.values)}
        if isinstance(node, ast.Compare) and len(node.ops) == 1:
            ops = {ast.Lt: sp.Lt, ast.LtE: sp.Le, ast.Gt: sp.Gt, ast.GtE: sp.Ge, ast.Eq: sp.Eq}
            if type(node.ops[0]) in ops:
                return ops[type(node.ops[0])](ev(node.left), ev(node.comparators[0]))
        if isinstance(node, ast.Subscript):
            base = ev(node.value)
            idx = ev(node.slice)
            try:
                return base[int(idx)] if not isinstance(base, dict) else base[idx]
            except Exception as e:  # noqa: BLE001
                raise CalcError(f"添字エラー: {e}") from None
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id not in funcs:
                raise CalcError(f"許可されていない関数: {node.func.id}")
            args = [ev(a) for a in node.args]
            kwargs = {}
            for kw in node.keywords:
                if kw.arg not in ("dict", "evaluate", "domain", "relational"):
                    raise CalcError(f"許可されていないキーワード引数: {kw.arg}")
                kwargs[kw.arg] = ev(kw.value) if not isinstance(kw.value, ast.Constant) or not isinstance(kw.value.value, bool) else kw.value.value
            return funcs[node.func.id](*args, **kwargs)
        raise CalcError(f"許可されていない構文: {type(node).__name__}")

    return ev(tree)


def _canon(v):
    import sympy as sp
    if isinstance(v, dict):
        return {str(k): _canon(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_canon(x) for x in v]
    if isinstance(v, sp.FiniteSet):
        return [_canon(x) for x in v]
    return v


def values_equal(a, b, mode: str) -> bool:
    import sympy as sp
    a, b = _canon(a), _canon(b)
    if isinstance(a, dict) or isinstance(b, dict):
        if not (isinstance(a, dict) and isinstance(b, dict)) or set(a) != set(b):
            return False
        return all(values_equal(a[k], b[k], mode) for k in a)
    if isinstance(a, list) or isinstance(b, list):
        if not isinstance(a, list):
            a = [a]
        if not isinstance(b, list):
            b = [b]
        if len(a) != len(b):
            return False
        if mode == "set":
            remaining = list(b)
            for x in a:
                for j, y in enumerate(remaining):
                    if values_equal(x, y, "value"):
                        remaining.pop(j)
                        break
                else:
                    return False
            return True
        return all(values_equal(x, y, mode) for x, y in zip(a, b))
    if isinstance(a, str) or isinstance(b, str):
        return str(a).strip() == str(b).strip()
    if isinstance(a, sp.Basic) and isinstance(a, sp.core.relational.Relational):
        return bool(sp.simplify(a.lhs - a.rhs - (b.lhs - b.rhs)) == 0) if isinstance(b, sp.core.relational.Relational) else False
    if isinstance(a, (sp.Set,)) or isinstance(b, (sp.Set,)):
        return a == b
    if mode == "numeric":
        da, db = complex(sp.N(a, 30)), complex(sp.N(b, 30))
        return abs(da - db) <= 1e-9 * max(1.0, abs(db))
    diff = sp.sympify(a) - sp.sympify(b)
    if mode == "expand":
        return sp.expand(diff) == 0
    if diff == 0:
        return True
    simp = sp.simplify(diff)
    if simp == 0:
        return True
    try:
        return bool(simp.is_zero) or (simp.is_number and abs(complex(sp.N(simp, 50))) < 1e-25)
    except (TypeError, ValueError):
        return False


class _Timeout(Exception):
    pass


def run_calc_check(check: dict, timeout: int = 10) -> str | None:
    """問題なければ None、不一致・評価失敗ならメッセージを返す。"""
    def handler(signum, frame):
        raise _Timeout()

    use_alarm = hasattr(signal, "SIGALRM")
    if use_alarm:
        old = signal.signal(signal.SIGALRM, handler)
        signal.alarm(timeout)
    try:
        got = safe_eval(check["expression"])
        exp = safe_eval(check["expected"])
        if not values_equal(got, exp, check.get("compare", "value")):
            return f"検算不一致: {check['expression']} = {got} ≠ 期待値 {check['expected']}"
        return None
    except _Timeout:
        return f"検算がタイムアウトしました（{timeout}秒）: {check['expression']}"
    except CalcError as e:
        return f"検算式を評価できません: {e}"
    except Exception as e:  # noqa: BLE001 sympy 内部の例外もまとめて報告
        return f"検算式の評価中にエラー: {type(e).__name__}: {e}"
    finally:
        if use_alarm:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old)


# --------------------------------------------------------------------------
# 類似度（重複検知）
# --------------------------------------------------------------------------

_STRIP = re.compile(r"[\s、。，．,.・「」『』（）()［］\[\]【】〈〉《》！？!?:：;；\"'“”‘’…]+")


def normalize_text(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\[\[(?:u|mark:[^:\]]*|blank):?([^\]]*)\]\]", r"\1", s)
    s = s.replace("\\,", "").replace("\\ ", "")
    s = _STRIP.sub("", s)
    return s.lower()


def shingles(s: str, n: int = 3) -> set[str]:
    if len(s) <= n:
        return {s} if s else set()
    return {s[i:i + n] for i in range(len(s) - n + 1)}


def fingerprint_text(q: dict) -> str:
    parts = [q.get("stem", "")]
    for c in q.get("choices", []) or []:
        parts.append(c.get("text", ""))
    return "\n".join(parts)


def find_similar(items: list[tuple[str, str, str]], threshold: float):
    """items: (key, display_id, text)。完全一致ペアと類似ペアを返す。

    完全一致は正規化テキストの SHA-256、類似は MinHash-LSH で候補を絞り、
    文字 3-gram の Jaccard 係数を正確に計算して threshold 以上を返す。
    """
    exact: dict[str, list[int]] = {}
    norm = []
    for idx, (_, _, text) in enumerate(items):
        n = normalize_text(text)
        norm.append(n)
        h = hashlib.sha256(n.encode()).hexdigest()
        exact.setdefault(h, []).append(idx)
    exact_pairs = []
    for idxs in exact.values():
        for a in range(len(idxs)):
            for b in range(a + 1, len(idxs)):
                exact_pairs.append((idxs[a], idxs[b]))
    exact_set = set(exact_pairs)

    num_perm, bands = 64, 16
    rows = num_perm // bands
    prime = (1 << 61) - 1
    coeffs = []
    seed = 1234567
    for _ in range(num_perm):
        seed = (seed * 6364136223846793005 + 1442695040888963407) % (1 << 64)
        a = seed % prime or 1
        seed = (seed * 6364136223846793005 + 1442695040888963407) % (1 << 64)
        coeffs.append((a, seed % prime))
    gram_hash: dict[str, int] = {}
    sh_sets = []
    buckets: dict[tuple, list[int]] = {}
    for idx, n in enumerate(norm):
        sh = shingles(n)
        sh_sets.append(sh)
        if not sh:
            continue
        hs = []
        for g in sh:
            h = gram_hash.get(g)
            if h is None:
                h = int.from_bytes(hashlib.blake2b(g.encode(), digest_size=8).digest(), "big")
                gram_hash[g] = h
            hs.append(h)
        sig = [min((a * h + b) % prime for h in hs) for a, b in coeffs]
        for band in range(bands):
            key = (band, tuple(sig[band * rows:(band + 1) * rows]))
            buckets.setdefault(key, []).append(idx)
    cand = set()
    for idxs in buckets.values():
        if len(idxs) > 1:
            for a in range(len(idxs)):
                for b in range(a + 1, len(idxs)):
                    cand.add((idxs[a], idxs[b]))
    similar = []
    for a, b in sorted(cand):
        if (a, b) in exact_set:
            continue
        sa, sb = sh_sets[a], sh_sets[b]
        if not sa or not sb:
            continue
        j = len(sa & sb) / len(sa | sb)
        if j >= threshold:
            similar.append((a, b, j))
    return exact_pairs, similar


# --------------------------------------------------------------------------
# 本体
# --------------------------------------------------------------------------

def load_curriculum() -> dict[str, dict]:
    m = json.loads(CURRICULUM_PATH.read_text(encoding="utf-8"))
    units = {}
    for st in m.get("stages", []):
        for s in st.get("subjects", []):
            for u in s.get("units", []):
                units[u["unit_id"]] = u
    for t in m.get("exam_tracks", []):
        for u in t.get("units", []):
            units[u["unit_id"]] = u
    return units


def content_hash(data: dict) -> str:
    body = {k: v for k, v in data.items() if k != "validation"}
    return hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def iter_strings(obj, path=()):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k == "svg":
                continue
            yield from iter_strings(v, path + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_strings(v, path + (i,))


_DISPLAY_MATH = re.compile(r"\$\$.*?\$\$", re.S)


def math_delimiters_balanced(s: str) -> bool:
    s = s.replace("\\$", "")
    s = _DISPLAY_MATH.sub("", s)
    return s.count("$") % 2 == 0


REQUIRED_Q_FIELDS = {
    "id": "問題ID",
    "answer": "正答",
    "explanation": "解説",
    "difficulty": "難易度",
    "scoring": "採点基準",
    "stem": "問題文",
    "unit_id": "単元",
    "skills": "技能",
    "verification": "検証状態",
    "copyright": "著作権状態",
}


def _empty(v) -> bool:
    if v is None:
        return True
    if isinstance(v, str):
        return not v.strip()
    if isinstance(v, (list, dict)):
        return len(v) == 0
    return False


def check_file(fr: FileResult, rep: Reporter, validator, units: dict, run_calc: bool, today: _dt.date) -> None:
    data = fr.data
    if not isinstance(data, dict):
        rep.add(fr, "ERROR", "schema", (), "トップレベルはオブジェクト（問題セット）でなければなりません")
        return

    # --- スキーマ ---
    for err in sorted(validator.iter_errors(data), key=lambda e: list(map(str, e.absolute_path))):
        rep.add(fr, "ERROR", "schema", tuple(err.absolute_path), _schema_message(err))

    set_id = data.get("set_id", "")
    questions = data.get("questions") if isinstance(data.get("questions"), list) else []

    # --- 必須フィールド（分かりやすいメッセージで個別に報告） ---
    for i, q in enumerate(questions):
        if not isinstance(q, dict):
            continue
        for key, label in REQUIRED_Q_FIELDS.items():
            if key not in q:
                rep.add(fr, "ERROR", "required", ("questions", i), f"必須フィールド「{label}」({key}) がありません（問題 {q.get('id', f'#{i + 1}')}）")
            elif _empty(q[key]):
                rep.add(fr, "ERROR", "required", ("questions", i, key), f"必須フィールド「{label}」({key}) が空です")
        ans = q.get("answer")
        if isinstance(ans, dict) and "value" in ans and _empty(ans["value"]):
            rep.add(fr, "ERROR", "required", ("questions", i, "answer", "value"), "正答の値が空です")

    # --- 文字化け・数式デリミタ ---
    for path, s in iter_strings(data):
        if "�" in s:
            rep.add(fr, "ERROR", "encoding", path, "置換文字 U+FFFD を含みます（文字化けの可能性）")
        if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", s):
            rep.add(fr, "ERROR", "encoding", path, "制御文字を含みます")
        if path and path[-1] in ("stem", "explanation", "text", "content", "display") and not math_delimiters_balanced(s):
            rep.add(fr, "ERROR", "latex", path, "数式デリミタ $ の数が対応していません")

    # --- 整合性 ---
    stim_ids = [s.get("id") for s in data.get("stimuli", []) if isinstance(s, dict)]
    for k, sid in enumerate(stim_ids):
        if stim_ids.count(sid) > 1 and stim_ids.index(sid) == k:
            rep.add(fr, "ERROR", "consistency", ("stimuli", k, "id"), f"資料ID {sid} が重複しています")
    sec_ids = {s.get("id") for s in data.get("sections", []) if isinstance(s, dict)}
    for k, sec in enumerate(data.get("sections", []) or []):
        for ref in sec.get("stimulus_refs", []) if isinstance(sec, dict) else []:
            if ref not in stim_ids:
                rep.add(fr, "ERROR", "consistency", ("sections", k, "stimulus_refs"), f"存在しない資料ID {ref} を参照しています")

    for u_i, uid in enumerate(data.get("unit_ids", []) or []):
        if isinstance(uid, str) and uid not in units:
            rep.add(fr, "ERROR", "curriculum", ("unit_ids", u_i), f"単元ID {uid} は curriculum_map.json に定義されていません")

    seen_ids: dict[str, int] = {}
    total = 0.0
    points_ok = True
    for i, q in enumerate(questions):
        if not isinstance(q, dict):
            continue
        qid = q.get("id", "")
        base = ("questions", i)
        if qid in seen_ids:
            rep.add(fr, "ERROR", "duplicate_id", base + ("id",), f"問題ID {qid} がファイル内で重複しています（{seen_ids[qid] + 1}問目と同じ）")
        else:
            seen_ids[qid] = i
        if set_id and isinstance(qid, str) and not qid.startswith(set_id + "-Q"):
            rep.add(fr, "ERROR", "consistency", base + ("id",), f"問題ID {qid} が set_id ({set_id}) で始まっていません")

        uid = q.get("unit_id")
        if isinstance(uid, str):
            u = units.get(uid)
            if u is None:
                rep.add(fr, "ERROR", "curriculum", base + ("unit_id",), f"単元ID {uid} は curriculum_map.json に定義されていません")
            else:
                if uid not in (data.get("unit_ids") or []):
                    rep.add(fr, "ERROR", "consistency", base + ("unit_id",), f"単元ID {uid} がセットの unit_ids に含まれていません")
                if u.get("subject") not in (None, q.get("subject")) and q.get("subject") != "integrated":
                    rep.add(fr, "WARNING", "curriculum", base + ("subject",), f"教科 {q.get('subject')} が単元 {uid} の教科 {u.get('subject')} と異なります")

        # 選択肢と正答
        qtype = q.get("question_type")
        choices = q.get("choices") or []
        labels = [c.get("label") for c in choices if isinstance(c, dict)]
        if len(labels) != len(set(labels)):
            rep.add(fr, "ERROR", "answer", base + ("choices",), "選択肢ラベルが重複しています")
        texts = [re.sub(r"\s+", "", unicodedata.normalize("NFKC", c.get("text", ""))) for c in choices if isinstance(c, dict)]
        if len(texts) != len(set(texts)):
            rep.add(fr, "ERROR", "answer", base + ("choices",), "同じ内容の選択肢があります")
        ans = q.get("answer") if isinstance(q.get("answer"), dict) else {}
        val = ans.get("value")
        if qtype in ("multiple_choice", "true_false") and labels:
            if not isinstance(val, (str, int)) or str(val) not in labels:
                rep.add(fr, "ERROR", "answer", base + ("answer", "value"), f"正答 {val!r} が選択肢ラベル {labels} に含まれていません")
        if qtype == "multiple_select" and labels and isinstance(val, list):
            bad = [v for v in val if str(v) not in labels]
            if bad:
                rep.add(fr, "ERROR", "answer", base + ("answer", "value"), f"正答 {bad} が選択肢ラベルにありません")
            if len(set(map(str, val))) != len(val):
                rep.add(fr, "ERROR", "answer", base + ("answer", "value"), "複数選択の正答が重複しています")
        if qtype == "ordering" and labels and isinstance(val, list):
            if sorted(map(str, val)) != sorted(labels):
                rep.add(fr, "ERROR", "answer", base + ("answer", "value"), "並べ替えの正答が選択肢をちょうど1回ずつ使っていません")
        if qtype not in ("multiple_choice", "multiple_select", "true_false", "ordering") and choices and not isinstance(val, (list,)) and str(val) in labels:
            rep.add(fr, "WARNING", "answer", base + ("question_type",), "選択肢と記号の正答がありますが question_type が選択式ではありません")

        # 参照
        ref = q.get("stimulus_ref")
        if ref and ref not in stim_ids:
            rep.add(fr, "ERROR", "consistency", base + ("stimulus_ref",), f"存在しない資料ID {ref} を参照しています")
        sec = q.get("section")
        if sec and sec not in sec_ids:
            rep.add(fr, "ERROR", "consistency", base + ("section",), f"存在しない大問ID {sec} を参照しています")

        # 配点
        sc = q.get("scoring") if isinstance(q.get("scoring"), dict) else {}
        pts = sc.get("points")
        if isinstance(pts, (int, float)):
            total += pts
        else:
            points_ok = False
        rub = sc.get("rubric")
        if isinstance(rub, list) and rub and isinstance(pts, (int, float)):
            rsum = sum(r.get("points", 0) for r in rub if isinstance(r, dict))
            if sc.get("method") == "rubric" and abs(rsum - pts) > 1e-9:
                rep.add(fr, "ERROR", "scoring", base + ("scoring", "rubric"), f"採点基準の合計 {rsum} が配点 {pts} と一致しません")
            if sc.get("method") == "partial" and rsum > pts + 1e-9:
                rep.add(fr, "ERROR", "scoring", base + ("scoring", "rubric"), f"部分点の合計 {rsum} が配点 {pts} を超えています")

        # 状態
        ver = q.get("verification") if isinstance(q.get("verification"), dict) else {}
        if ver.get("status") == "draft":
            rep.add(fr, "WARNING", "verification", base + ("verification", "status"), "検証状態が draft（未検査）のままです")
        if ver.get("status") == "rejected":
            rep.add(fr, "ERROR", "verification", base + ("verification", "status"), "差し戻し（rejected）の問題が含まれています")
        cp = q.get("copyright") if isinstance(q.get("copyright"), dict) else {}
        if cp.get("status") == "needs_clearance":
            rep.add(fr, "WARNING", "copyright", base + ("copyright", "status"), "権利処理が未完了です（公開・配布不可）")

        # 検算
        cc = q.get("calc_check")
        if run_calc and isinstance(cc, dict) and "expression" in cc and "expected" in cc:
            msg = run_calc_check(cc)
            if msg:
                rep.add(fr, "ERROR", "calc_check", base + ("calc_check",), msg)

    tp = data.get("total_points")
    if isinstance(tp, (int, float)) and points_ok and questions and abs(tp - total) > 1e-9:
        rep.add(fr, "ERROR", "scoring", ("total_points",), f"total_points {tp} と各問の配点合計 {total:g} が一致しません")

    # 変更履歴
    hist = data.get("revision_history") or []
    prev = None
    for k, h in enumerate(hist):
        if not isinstance(h, dict):
            continue
        v = h.get("version", "")
        if re.fullmatch(r"\d+\.\d+\.\d+", str(v)):
            tv = tuple(int(x) for x in v.split("."))
            if prev and tv <= prev:
                rep.add(fr, "ERROR", "revision", ("revision_history", k, "version"), f"バージョン {v} が前の記録より大きくありません")
            prev = tv
        d = h.get("date")
        try:
            if d and _dt.date.fromisoformat(d) > today:
                rep.add(fr, "ERROR", "revision", ("revision_history", k, "date"), f"日付 {d} が未来です")
        except ValueError:
            rep.add(fr, "ERROR", "revision", ("revision_history", k, "date"), f"日付 {d} が不正です")


def _schema_message(err) -> str:
    v = err.validator
    if v == "required":
        return f"必須項目がありません: {err.message}"
    if v == "additionalProperties":
        return f"定義されていない項目があります: {err.message}"
    if v == "enum":
        return f"許可されていない値です: {err.instance!r}（許可: {err.validator_value}）"
    if v == "pattern":
        return f"形式が不正です: {err.instance!r}（パターン {err.validator_value}）"
    return err.message


def collect_files(targets: list[str]) -> list[Path]:
    files: list[Path] = []
    for t in targets:
        p = Path(t)
        if not p.is_absolute():
            p = (Path.cwd() / p).resolve()
        if p.is_dir():
            files.extend(sorted(x for x in p.rglob("*.json") if x.is_file()))
        elif p.is_file():
            files.append(p)
        else:
            raise FileNotFoundError(t)
    seen, out = set(), []
    for f in files:
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out


def relpath(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def validate_paths(targets: list[str], similarity: float = 0.85, run_calc: bool = True,
                   corpus: list[str] | None = None) -> Reporter:
    """targets を検査する。corpus を指定すると、重複検知はそのファイル群も含めて行う
    （targets 以外のファイルの問題そのものは報告しない）。"""
    from jsonschema import Draft202012Validator, FormatChecker

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    units = load_curriculum()
    today = _dt.date.today()
    rep = Reporter()

    target_files = collect_files(targets)
    corpus_files = collect_files(corpus) if corpus else []
    target_set = set(target_files)

    loaded: list[FileResult] = []
    for path in target_files + [c for c in corpus_files if c not in target_set]:
        fr = FileResult(path=path, rel=relpath(path))
        is_target = path in target_set
        try:
            raw = path.read_bytes()
            text = raw.decode("utf-8")
            if text.startswith("﻿"):
                rep.add(fr, "WARNING", "encoding", (), "BOM 付き UTF-8 です（BOM なしを推奨）")
                text = text[1:]
        except UnicodeDecodeError as e:
            fr.issues.append(Issue("ERROR", fr.rel, None, "encoding", "", f"UTF-8 として読めません（{e.start} バイト目）"))
            if is_target:
                rep.files.append(fr)
            continue
        try:
            fr.data = json.loads(text)
        except json.JSONDecodeError as e:
            fr.issues.append(Issue("ERROR", fr.rel, e.lineno, "json_syntax", "", f"JSON 構文エラー: {e.msg}（{e.lineno}行 {e.colno}列）"))
            if is_target:
                rep.files.append(fr)
            continue
        try:
            fr.positions = _PosParser(text).parse()
        except Exception:  # noqa: BLE001 位置情報が取れなくても検査は続行
            fr.positions = {}
        if is_target:
            check_file(fr, rep, validator, units, run_calc, today)
            rep.files.append(fr)
        loaded.append((fr, is_target))

    # --- ID の全体重複・類似問題 ---
    items = []
    owners = []
    id_owner: dict[str, tuple[FileResult, int]] = {}
    for fr, is_target in loaded:
        qs = fr.data.get("questions") if isinstance(fr.data, dict) else None
        if not isinstance(qs, list):
            continue
        for i, q in enumerate(qs):
            if not isinstance(q, dict):
                continue
            qid = q.get("id")
            if isinstance(qid, str):
                if qid in id_owner and id_owner[qid][0] is not fr:
                    ofr, oi = id_owner[qid]
                    if is_target:
                        rep.add(fr, "ERROR", "duplicate_id", ("questions", i, "id"), f"問題ID {qid} が {ofr.rel} と重複しています")
                else:
                    id_owner.setdefault(qid, (fr, i))
            items.append((fr.rel, qid or f"#{i + 1}", fingerprint_text(q)))
            owners.append((fr, i, is_target))
    exact, similar = find_similar(items, similarity)
    for a, b in exact:
        fa, ia, ta = owners[a]
        fb, ib, tb = owners[b]
        if not (ta or tb):
            continue
        fr, i, other = (fb, ib, a) if tb else (fa, ia, b)
        rep.add(fr, "ERROR", "duplicate", ("questions", i), f"問題 {items[b if tb else a][1]} は {items[other][0]} の {items[other][1]} と同一の問題文です")
    for a, b, j in similar:
        fa, ia, ta = owners[a]
        fb, ib, tb = owners[b]
        if not (ta or tb):
            continue
        fr, i, other = (fb, ib, a) if tb else (fa, ia, b)
        rep.add(fr, "WARNING", "similar", ("questions", i), f"問題 {items[b if tb else a][1]} は {items[other][0]} の {items[other][1]} と類似しています（類似度 {j:.2f}）")
    return rep


def stamp_files(rep: Reporter) -> None:
    now = _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()
    for fr in rep.files:
        if not isinstance(fr.data, dict) or any(i.category in ("json_syntax", "encoding") for i in fr.issues if i.level == "ERROR"):
            continue
        result = "fail" if fr.errors else ("pass_with_warnings" if fr.warnings else "pass")
        data = dict(fr.data)
        data["validation"] = {
            "validated_at": now,
            "validator_version": VALIDATOR_VERSION,
            "result": result,
            "errors": fr.errors,
            "warnings": fr.warnings,
            "content_hash": content_hash(data),
        }
        fr.path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def print_report(rep: Reporter, quiet: bool = False, max_per_file: int = 200) -> None:
    for fr in rep.files:
        if fr.issues:
            shown = sorted(fr.issues, key=lambda i: (i.level != "ERROR", i.line or 0))
            for iss in shown[:max_per_file]:
                print(iss.format())
            if len(shown) > max_per_file:
                print(f"{fr.rel}: ... ほか {len(shown) - max_per_file} 件")
    if quiet:
        return
    print()
    print(f"{'ファイル':<58} {'問題数':>5} {'エラー':>6} {'警告':>5}")
    print("-" * 78)
    nq = 0
    for fr in rep.files:
        n = len(fr.data.get("questions", [])) if isinstance(fr.data, dict) and isinstance(fr.data.get("questions"), list) else 0
        nq += n
        mark = "NG" if fr.errors else ("△" if fr.warnings else "OK")
        print(f"{fr.rel:<58} {n:>5} {fr.errors:>6} {fr.warnings:>5}  {mark}")
    errs = sum(f.errors for f in rep.files)
    warns = sum(f.warnings for f in rep.files)
    print("-" * 78)
    print(f"合計 {len(rep.files)} ファイル / {nq} 問 / エラー {errs} 件 / 警告 {warns} 件")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="問題データ JSON の自動検査")
    ap.add_argument("paths", nargs="*", help="検査するファイルまたはディレクトリ（既定: data/）")
    ap.add_argument("--corpus", nargs="*", default=None, help="重複検知の比較対象に加えるファイル・ディレクトリ")
    ap.add_argument("--similarity", type=float, default=0.85, help="類似問題とみなす Jaccard 係数の閾値（既定 0.85）")
    ap.add_argument("--strict", action="store_true", help="警告もエラーとして扱う")
    ap.add_argument("--no-calc", action="store_true", help="検算（calc_check）を省略する")
    ap.add_argument("--stamp", action="store_true", help="検査結果を各ファイルの validation に書き込む")
    ap.add_argument("--report", help="結果を JSON で保存するパス")
    ap.add_argument("--quiet", action="store_true", help="サマリー表を表示しない")
    args = ap.parse_args(argv)

    targets = args.paths or [str(DEFAULT_DATA_DIR)]
    try:
        rep = validate_paths(targets, args.similarity, not args.no_calc, args.corpus)
    except FileNotFoundError as e:
        print(f"ERROR: パスが見つかりません: {e}", file=sys.stderr)
        return 2
    print_report(rep, args.quiet)
    if args.stamp:
        stamp_files(rep)
    if args.report:
        Path(args.report).write_text(json.dumps({
            "validator_version": VALIDATOR_VERSION,
            "issues": [i.__dict__ for i in rep.all_issues],
            "files": [{"file": f.rel, "errors": f.errors, "warnings": f.warnings} for f in rep.files],
        }, ensure_ascii=False, indent=2), encoding="utf-8")
    errs = sum(f.errors for f in rep.files)
    warns = sum(f.warnings for f in rep.files)
    if errs or (args.strict and warns):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
