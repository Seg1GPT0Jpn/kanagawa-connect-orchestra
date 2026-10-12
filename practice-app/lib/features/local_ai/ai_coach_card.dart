import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../../app/app_services.dart';
import '../../core/clock.dart';
import '../menu/domain/menu_proposal.dart';
import '../menu/domain/rule_based_plan.dart';
import '../practice/domain/day_condition.dart';
import '../practice/domain/practice_stats.dart';
import 'local_ai_service.dart';
import 'practice_coach.dart';

/// 練習タブの「練習コーチ」。内蔵の AI が使えれば相談でき、使えなくても記録からルールで提案する
class AiCoachCard extends StatefulWidget {
  const AiCoachCard({super.key, required this.stats});

  final PracticeStats stats;

  @override
  State<AiCoachCard> createState() => _AiCoachCardState();
}

class _AiCoachCardState extends State<AiCoachCard> {
  late final AppServices _services = AppScope.of(context);
  LocalAiState? _state;
  bool _busy = false;
  int? _progress;
  String? _error;
  String? _advice;
  MenuProposalReview? _proposal;
  RuleBasedPlan? _rulePlan;

  bool _probing = false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (_state != null || _probing) return;
    _probing = true;
    _services.localAi.probe().then((s) {
      if (!mounted) return;
      setState(
        () => _state = _services.localAi.isSupported ? LocalAiState.ready : s,
      );
    });
  }

  Future<CoachContext> _context() async {
    final menu = _services.menu;
    return CoachContext(
      rules: menu.rules,
      currentMenu: menu.value,
      condition: await _services.dayConditions.load(
        localDateString(_services.clock()),
      ),
      stats: widget.stats,
    );
  }

  Future<void> _run(Future<void> Function() task) async {
    setState(() {
      _busy = true;
      _error = null;
    });
    try {
      await task();
    } on LocalAiException catch (e) {
      _error = e.message;
    } finally {
      if (mounted) {
        setState(() {
          _busy = false;
          _progress = null;
        });
      }
    }
  }

  Future<void> _prepare() => _run(() async {
    await _services.localAi.initializeModel(
      onProgress: (p) {
        if (mounted) setState(() => _progress = p);
      },
    );
    _state = LocalAiState.ready;
  });

  Future<void> _askMenu() => _run(() async {
    final ctx = await _context();
    _proposal = await PracticeCoach(_services.localAi).suggestMenu(ctx);
    _advice = null;
    _rulePlan = null;
  });

  Future<void> _askAdvice() => _run(() async {
    final ctx = await _context();
    if (adviseForDay(ctx.condition).rest) {
      _advice = '今日は唇を休ませましょう。痛みが続くときは、指導者や医療機関に相談してください。';
    } else {
      _advice = await PracticeCoach(_services.localAi).advice(ctx);
    }
    _proposal = null;
    _rulePlan = null;
  });

  /// AI を使わずに、記録の偏りからメニューを調整する（いつでも使える）
  void _askRules() {
    final menu = _services.menu;
    setState(() {
      _rulePlan = planMenuByRules(
        rules: menu.rules,
        currentMenu: menu.value,
        secondsLast7: widget.stats.secondsByItemLast7,
      );
      _proposal = null;
      _advice = null;
      _error = null;
    });
  }

  void _use(Map<String, int> minutes, String what) {
    final menu = _services.menu;
    menu.useForToday(menu.rules.id, minutes);
    setState(() {
      _proposal = null;
      _rulePlan = null;
    });
    ScaffoldMessenger.of(context)
        .showSnackBar(SnackBar(content: Text('$whatを今日のメニューにしました')));
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final state = _state;
    if (state == null) return const SizedBox.shrink();
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.auto_awesome_outlined, size: 20),
                const SizedBox(width: 8),
                Text('練習コーチ', style: theme.textTheme.titleMedium),
              ],
            ),
            const SizedBox(height: 8),
            switch (state) {
              LocalAiState.unavailable => Text(
                'この端末・ブラウザでは、内蔵の AI を使えません。代わりに、記録の偏りからルールで提案できます。',
                style: theme.textTheme.bodySmall,
              ),
              LocalAiState.needsPreparation || LocalAiState.preparing => Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '端末に内蔵の AI を使えます。最初だけ、端末（ブラウザ）が AI を準備します（大きなダウンロードになることがあるので、Wi-Fi で）。',
                    style: theme.textTheme.bodySmall,
                  ),
                  const SizedBox(height: 8),
                  if (_busy)
                    LinearProgressIndicator(
                      value: _progress == null ? null : _progress! / 100,
                    ),
                  if (!_busy)
                    FilledButton.tonal(
                      onPressed: _prepare,
                      child: const Text('AI を準備する'),
                    ),
                ],
              ),
              LocalAiState.ready => Wrap(
                spacing: 8,
                runSpacing: 4,
                children: [
                  FilledButton.tonal(
                    onPressed: _busy
                        ? null
                        : (_services.localAi.isSupported
                              ? _askMenu
                              : () => _prepareThen(_askMenu)),
                    child: const Text('メニューを相談'),
                  ),
                  OutlinedButton(
                    onPressed: _busy
                        ? null
                        : (_services.localAi.isSupported
                              ? _askAdvice
                              : () => _prepareThen(_askAdvice)),
                    child: const Text('ひとことアドバイス'),
                  ),
                ],
              ),
            },
            if (_busy && state == LocalAiState.ready) ...[
              const SizedBox(height: 8),
              const LinearProgressIndicator(),
            ],
            if (_error != null) ...[
              const SizedBox(height: 8),
              Text(_error!, style: TextStyle(color: theme.colorScheme.error)),
            ],
            const SizedBox(height: 8),
            OutlinedButton.icon(
              onPressed: _busy ? null : _askRules,
              icon: const Icon(Icons.rule, size: 18),
              label: const Text('記録から提案（AI なし）'),
            ),
            if (_advice != null) ...[const SizedBox(height: 8), Text(_advice!)],
            if (_proposal != null) ..._proposalView(_proposal!, theme),
            if (_rulePlan != null) ..._rulePlanView(_rulePlan!, theme),
            const SizedBox(height: 8),
            Text(
              'AI は端末の中だけで動き、記録は外に送りません。どの案も、時間のルールをアプリが確かめてから使います。',
              style: theme.textTheme.bodySmall,
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _prepareThen(Future<void> Function() next) async {
    await _prepare();
    if (_services.localAi.isSupported) await next();
  }

  String _describe(Map<String, int> m) {
    final rules = _services.menu.rules;
    return [
      for (final item in rules.items)
        if ((m[item.id] ?? 0) > 0) '${rules.labelOf(item.id)} ${m[item.id]}分',
    ].join('・');
  }

  List<Widget> _rulePlanView(RuleBasedPlan p, ThemeData theme) {
    final total = p.minutes.values.fold(0, (s, v) => s + v);
    final same = mapEquals(p.minutes, {
      for (final item in _services.menu.rules.items)
        item.id: _services.menu.value[item.id] ?? 0,
    });
    return [
      const SizedBox(height: 8),
      Text('記録からの提案（合計$total分）', style: theme.textTheme.titleSmall),
      Text(_describe(p.minutes)),
      const SizedBox(height: 4),
      Text('理由', style: theme.textTheme.labelLarge),
      for (final r in p.reasons) Text('・$r'),
      if (!same) ...[
        const SizedBox(height: 8),
        FilledButton(
          onPressed: () => _use(p.minutes, '提案'),
          child: const Text('今日はこの案にする'),
        ),
      ],
    ];
  }

  List<Widget> _proposalView(MenuProposalReview p, ThemeData theme) {
    final describe = _describe;
    if (p.parseError != null) {
      return [
        const SizedBox(height: 8),
        Text(
          'AI の答えを読み取れませんでした（${p.parseError}）。もう一度お試しください。',
          style: TextStyle(color: theme.colorScheme.error),
        ),
      ];
    }
    final menu = p.isAcceptable ? p.minutes! : p.correction!;
    final total = menu.values.fold(0, (s, v) => s + v);
    return [
      const SizedBox(height: 8),
      Text('AI の案（合計$total分）', style: theme.textTheme.titleSmall),
      Text(describe(menu)),
      if (p.reason != null) ...[
        const SizedBox(height: 4),
        Text('AI が考えた理由：${p.reason}'),
      ],
      if (!p.isAcceptable) ...[
        const SizedBox(height: 4),
        Text(
          'AI の案はルールに合わなかったので、アプリが直しました：${p.audit!.violations.map((v) => v.message).join('、')}',
          style: theme.textTheme.bodySmall?.copyWith(
            color: theme.colorScheme.error,
          ),
        ),
      ],
      const SizedBox(height: 8),
      FilledButton(
        onPressed: () => _use(menu, 'AI の案'),
        child: const Text('今日はこの案にする'),
      ),
    ];
  }
}
