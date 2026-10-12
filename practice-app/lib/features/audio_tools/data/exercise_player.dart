import 'dart:async';

import 'package:flutter/foundation.dart';

import 'reference_tone_controller.dart';

/// 練習音型を、テンポに合わせて基準音で順に鳴らす（音の高さの目安。リズムの正確さはメトロノームで）
class ExercisePlayer extends ChangeNotifier {
  ExercisePlayer(this._tone);

  final ReferenceToneController _tone;
  Timer? _timer;
  List<int> _written = const [];
  int _index = -1;
  bool _loop = false;

  bool get isPlaying => _timer != null;

  /// いま鳴らしている音の位置（止まっていれば -1）
  int get index => _index;
  List<int> get notes => _written;

  /// [written]（記譜）を [bpm] の速さで、1音 [beats] 拍ずつ鳴らす。
  /// ボタンの処理から直接呼ぶ（最初の音は待たずに鳴らす）
  Future<void> play(
    List<int> written, {
    required int bpm,
    int beats = 1,
    bool loop = false,
  }) {
    stop();
    if (written.isEmpty) return Future.value();
    _written = written;
    _loop = loop;
    _index = 0;
    final step = Duration(microseconds: (60000000 / bpm * beats).round());
    final first = _sound(0);
    _timer = Timer.periodic(step, (_) => _advance());
    notifyListeners();
    return first;
  }

  Future<void> _sound(int i) {
    final t = _tone.pitch.transposition;
    return _tone.playConcert(t.writtenToConcert(_written[i]));
  }

  void _advance() {
    var next = _index + 1;
    if (next >= _written.length) {
      if (!_loop) {
        stop();
        return;
      }
      next = 0;
    }
    _index = next;
    unawaited(_sound(next));
    notifyListeners();
  }

  void stop() {
    final wasPlaying = _timer != null;
    _timer?.cancel();
    _timer = null;
    _index = -1;
    if (wasPlaying) {
      _tone.stop();
      notifyListeners();
    }
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }
}
