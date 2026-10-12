import 'dart:async';
import 'dart:typed_data';

import 'package:kco_practice/features/audio_tools/data/audio_engine.dart';
import 'package:kco_practice/features/audio_tools/data/mic_input.dart';
import 'package:kco_practice/features/audio_tools/domain/metronome.dart';
import 'package:kco_practice/features/audio_tools/domain/sound.dart';
import 'package:kco_practice/features/auth/auth_service.dart';
import 'package:kco_practice/features/data_io/data_io_service.dart';
import 'package:kco_practice/features/local_ai/local_ai_service.dart';
import 'package:kco_practice/features/practice/domain/practice_record.dart';
import 'package:kco_practice/features/sync/conflict.dart';
import 'package:kco_practice/features/sync/remote_record_store.dart';
import 'package:sembast/sembast_memory.dart';

/// テストごとに別の、メモリ上のデータベース
Future<Database> openMemoryDb() =>
    newDatabaseFactoryMemory().openDatabase('test.db');

/// 手で進める時計
class FakeClock {
  FakeClock([DateTime? start]) : now = start ?? DateTime(2026, 10, 12, 9);

  DateTime now;
  DateTime call() => now;
  void advance(Duration d) => now = now.add(d);
}

PracticeRecord record(
  String id, {
  String? owner = 'u1',
  int updatedAt = 1000,
  String by = 'devA',
  bool deleted = false,
  String note = '',
  String day = '2026-10-12',
  Map<String, int> actual = const {'mouthpiece': 1200},
}) => PracticeRecord(
  id: id,
  ownerUid: owner,
  practicedOn: day,
  startedAtMillis: 0,
  ruleSetId: 'trumpet_basic',
  plannedMinutes: const {'mouthpiece': 20},
  actualSeconds: actual,
  note: note,
  updatedAtMillis: updatedAt,
  updatedBy: by,
  deleted: deleted,
);

/// Firestore の代わり（FirestoreRemoteRecordStore と同じ決まりで動く）
class FakeRemote implements RemoteRecordStore {
  final Map<String, Map<String, (PracticeRecord, int)>> data = {};
  int serverTime = 100;
  bool offline = false;
  int fetchCount = 0;

  /// 送信の直前に割り込む処理（送っている間に別の端末が書き込んだ、などを再現する）
  Future<void> Function()? beforePush;

  void putServer(String uid, PracticeRecord r) =>
      (data[uid] ??= {})[r.id] = (r, serverTime++);

  PracticeRecord? get(String uid, String id) => data[uid]?[id]?.$1;

  @override
  Future<RemoteChanges> fetchChangedSince(String uid, int? cursorMillis) async {
    if (offline) throw StateError('offline');
    fetchCount++;
    final hits =
        (data[uid] ?? {}).values
            .where((e) => cursorMillis == null || e.$2 >= cursorMillis)
            .toList()
          ..sort((a, b) => a.$2.compareTo(b.$2));
    return RemoteChanges([
      for (final e in hits) e.$1,
    ], hits.isEmpty ? null : hits.last.$2);
  }

  @override
  Future<PracticeRecord> pushIfNewer(String uid, PracticeRecord record) async {
    if (offline) throw StateError('offline');
    await beforePush?.call();
    final existing = get(uid, record.id);
    if (existing != null &&
        identical(resolveConflict(record, existing), existing)) {
      return existing;
    }
    putServer(uid, record);
    return record;
  }
}

class FakeAuth implements AuthService {
  FakeAuth([this._user]);

  AppUser? _user;
  final _controller = StreamController<AppUser?>.broadcast();

  void emit(AppUser? u) {
    _user = u;
    _controller.add(u);
  }

  @override
  AppUser? get currentUser => _user;

  @override
  Stream<AppUser?> get userChanges => _controller.stream;

  @override
  Future<void> signInWithGoogle() async =>
      emit(const AppUser(uid: 'u1', email: 'u1@example.com'));

  @override
  Future<void> signInWithEmail(String email, String password) async {
    if (password != 'secret1') throw const AuthFailure('メールアドレスかパスワードが違います');
    emit(AppUser(uid: 'u-$email', email: email));
  }

  @override
  Future<void> signUpWithEmail(String email, String password) =>
      signInWithEmail(email, password);

  @override
  Future<void> sendPasswordReset(String email) async {}

  @override
  Future<void> signOut() async => emit(null);
}

/// 音を鳴らさない AudioEngine（予約・正弦波を記録する。時計は手で進める）
class FakeAudioEngine implements AudioEngine {
  FakeAudioEngine({this.failToStart = false});

  final bool failToStart;
  bool started = false;
  Duration time = Duration.zero;
  final List<(ClickKind, Duration)> scheduled = [];
  int cancelCount = 0;
  double? toneHz;
  double? toneVolume;

  @override
  Future<void> ensureStarted() async {
    if (failToStart) throw const AudioEngineException('音を出せませんでした');
    started = true;
  }

  @override
  bool get isStarted => started;

  @override
  Duration get now => time;

  @override
  void scheduleClick(
    ClickKind kind,
    Duration at, {
    ClickSound sound = ClickSound.beep,
    double volume = 1,
  }) {
    scheduled.add((kind, at));
    clickSounds.add(sound);
    clickVolumes.add(volume);
  }

  final List<ClickSound> clickSounds = [];
  final List<double> clickVolumes = [];

  @override
  void cancelScheduledClicks() {
    cancelCount++;
    // まだ鳴っていない予約を消す
    scheduled.removeWhere((c) => c.$2 > time);
  }

  @override
  Future<void> startTone(
    double hz, {
    double volume = 0.5,
    Timbre timbre = Timbre.sine,
    int voice = 0,
  }) async {
    await ensureStarted();
    voices[voice] = (hz: hz, volume: volume, timbre: timbre);
    if (voice == 0) {
      toneHz = hz;
      toneVolume = volume;
    }
  }

  /// 鳴っている音（番号ごと）
  final Map<int, ({double hz, double volume, Timbre timbre})> voices = {};

  @override
  void stopTone({int? voice}) {
    if (voice == null) {
      voices.clear();
    } else {
      voices.remove(voice);
    }
    if (voice == null || voice == 0) toneHz = null;
  }

  Uint8List? playedWav;
  void Function()? onPlaybackDone;

  @override
  Future<void> playWav(
    Uint8List wav, {
    double speed = 1,
    void Function()? onDone,
  }) async {
    await ensureStarted();
    playedWav = wav;
    playbackSpeed = speed;
    onPlaybackDone = onDone;
  }

  double playbackSpeed = 1;
  final Map<AudioChannel, double> channelVolumes = {};

  @override
  double volumeOf(AudioChannel channel) => channelVolumes[channel] ?? 1;

  @override
  void setVolume(AudioChannel channel, double volume) =>
      channelVolumes[channel] = volume;

  @override
  void stopPlayback() {
    playedWav = null;
    onPlaybackDone = null;
  }
}

/// 音を受け取らないマイク（テストから波形を流し込む）
class FakeMicInput implements MicInput {
  FakeMicInput({this.allowed = true});

  bool allowed;
  bool running = false;
  int? sampleRate;
  StreamController<Float64List>? _controller;

  void push(Float64List samples) => _controller?.add(samples);

  @override
  Future<bool> requestPermission() async => allowed;

  @override
  Future<Stream<Float64List>> start({required int sampleRate}) async {
    this.sampleRate = sampleRate;
    running = true;
    _controller = StreamController<Float64List>();
    return _controller!.stream;
  }

  @override
  Future<void> stop() async {
    running = false;
    await _controller?.close();
    _controller = null;
  }
}

/// 決まった答えを返す AI（指示文を記録する）
class FakeLocalAiService implements LocalAiService {
  FakeLocalAiService({this.state = LocalAiState.ready, List<String>? replies})
    : replies = replies ?? [];

  LocalAiState state;
  final List<String> replies;
  final List<String> prompts = [];
  final List<String?> systemInstructions = [];
  bool initialized = false;

  @override
  bool get isSupported => initialized;

  @override
  Future<LocalAiState> probe() async => state;

  @override
  Future<void> initializeModel({void Function(int percent)? onProgress}) async {
    if (state == LocalAiState.unavailable) {
      throw const LocalAiException('使えません');
    }
    onProgress?.call(100);
    initialized = true;
    state = LocalAiState.ready;
  }

  @override
  Future<String> generatePrompt(
    String promptText, {
    String? systemInstruction,
  }) async {
    if (!initialized) throw const LocalAiException('AI の準備ができていません');
    prompts.add(promptText);
    systemInstructions.add(systemInstruction);
    if (replies.isEmpty) throw const LocalAiException('答えがありません');
    return replies.removeAt(0);
  }
}

/// ファイルを実際には保存・選択しない（保存した内容を記録し、選ぶファイルを渡せる）
class FakeFileGateway implements FileGateway {
  final Map<String, (Uint8List, String)> saved = {};
  Uint8List? toPick;
  bool cancel = false;

  @override
  Future<bool> save(
    String fileName,
    Uint8List bytes, {
    required String mimeType,
  }) async {
    if (cancel) return false;
    saved[fileName] = (bytes, mimeType);
    return true;
  }

  @override
  Future<Uint8List?> pickJson() async => cancel ? null : toPick;
}
