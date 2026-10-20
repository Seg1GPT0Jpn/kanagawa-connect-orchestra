import 'package:flutter/foundation.dart';

import '../../../core/meta_store.dart';
import '../domain/metronome.dart';
import '../domain/sound.dart';
import 'audio_engine.dart';

/// 系統ごとの音量（ミキサー）と、音のテスト
class MixerController extends ChangeNotifier {
  MixerController(this._engine, this._meta);

  static Future<MixerController> load(
    AudioEngine engine,
    MetaStore meta,
  ) async {
    final c = MixerController(engine, meta);
    final raw = await meta.get('audio.volumes');
    if (raw is Map) {
      for (final ch in AudioChannel.values) {
        final v = raw[ch.name];
        if (v is num) engine.setVolume(ch, v.toDouble());
      }
    }
    return c;
  }

  final AudioEngine _engine;
  final MetaStore _meta;
  String? _testResult;
  bool _testing = false;

  double volumeOf(AudioChannel channel) => _engine.volumeOf(channel);

  /// 最後の音のテストの結果（null は未実施）
  String? get testResult => _testResult;
  bool get isTesting => _testing;

  Future<void> setVolume(AudioChannel channel, double volume) async {
    _engine.setVolume(channel, volume);
    notifyListeners();
    await _meta.put('audio.volumes', {
      for (final c in AudioChannel.values) c.name: _engine.volumeOf(c),
    });
  }

  /// テスト音（クリック3回）を鳴らす。ボタンの処理から直接呼ぶこと
  Future<void> playTest() async {
    _testing = true;
    notifyListeners();
    try {
      await _engine.ensureStarted();
      final t = _engine.now + const Duration(milliseconds: 80);
      for (var i = 0; i < 3; i++) {
        _engine.scheduleClick(
          i == 0 ? ClickKind.accent : ClickKind.beat,
          t + Duration(milliseconds: 400 * i),
        );
      }
      _testResult = volumeOf(AudioChannel.click) == 0
          ? 'メトロノームの音量が 0 です。下のつまみで上げてください'
          : 'テスト音を3回鳴らしました。聞こえない場合は、下の点を確かめてください';
    } on AudioEngineException catch (e) {
      _testResult = e.message;
    } finally {
      _testing = false;
      notifyListeners();
    }
  }
}
