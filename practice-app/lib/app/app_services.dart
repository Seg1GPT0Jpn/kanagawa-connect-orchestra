import 'dart:async';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/widgets.dart';
import 'package:sembast/sembast.dart';

import '../core/clock.dart';
import '../core/local_database.dart';
import '../core/meta_store.dart';
import '../features/audio_tools/data/audio_engine.dart';
import '../features/audio_tools/data/metronome_controller.dart';
import '../features/audio_tools/data/mic_input.dart';
import '../features/audio_tools/data/reference_tone_controller.dart';
import '../features/audio_tools/data/tuner_controller.dart';
import '../features/auth/auth_service.dart';
import '../features/auth/firebase_auth_service.dart';
import '../features/local_ai/local_ai_service.dart';
import '../features/menu/data/practice_menu_controller.dart';
import '../features/menu/data/menu_settings_repository.dart';
import '../features/menu/domain/menu_rules.dart';
import '../features/practice/data/day_condition_repository.dart';
import '../features/practice/data/practice_repository.dart';
import '../features/sync/firestore_remote_record_store.dart';
import '../features/sync/remote_record_store.dart';
import '../features/sync/sync_controller.dart';
import '../features/sync/sync_engine.dart';
import '../firebase_options.dart';

/// アプリ全体で使う部品（依存関係の注入）
class AppServices {
  AppServices({
    required this.practice,
    required this.menu,
    required this.dayConditions,
    required this.audio,
    required this.metronome,
    required this.referenceTone,
    required this.tuner,
    required this.sync,
    required this.localAi,
    this.clock = systemClock,
  });

  final PracticeRepository practice;
  final PracticeMenuController menu;

  /// 今日の予定と調子（端末内だけ）
  final DayConditionRepository dayConditions;

  /// 音を鳴らす（メトロノーム・基準音）
  final AudioEngine audio;
  final MetronomeController metronome;

  /// 基準ピッチ（A4）・楽器の調と基準音
  final ReferenceToneController referenceTone;
  final TunerController tuner;

  /// クラウド同期（ログインもここから使う。sync.auth）
  final SyncController sync;
  final LocalAiService localAi;
  final Clock clock;

  /// 端末内のデータベースを開いてすぐ返す。クラウド（Firebase）には裏でつなぐ
  ///
  /// Firebase の読み込みを待たないのは、オフラインだと読み込みが終わらず、
  /// 画面が出なくなるため。つながらなくても端末内の保存だけで使える。
  static Future<AppServices> create() async {
    final services = await fromParts(db: await openLocalDatabase());
    unawaited(services._connectCloud());
    return services;
  }

  /// Firebase の初期化を待つ上限
  static const cloudTimeout = Duration(seconds: 15);

  Future<void> _connectCloud() async {
    // Firebase に未登録の端末（Android・iOS）は unavailable のまま
    if (DefaultFirebaseOptions.currentPlatform == null) return;
    sync.beginConnecting();
    final ok = await _initFirebase().timeout(
      cloudTimeout,
      onTimeout: () => false,
    );
    if (!ok) {
      sync.markUnavailable();
      return;
    }
    sync.attach(
      FirebaseAuthService(FirebaseAuth.instance),
      SyncEngine(
        practice,
        FirestoreRemoteRecordStore(FirebaseFirestore.instance),
      ),
    );
  }

  /// テストでは authOverride・remoteOverride（偽物）を渡すと、最初からクラウドにつながった状態になる
  static Future<AppServices> fromParts({
    required Database db,
    AuthService? authOverride,
    RemoteRecordStore? remoteOverride,
    AudioEngine? audioOverride,
    MicInput? micOverride,
    Clock clock = systemClock,
  }) async {
    final meta = MetaStore(db);
    final practice = PracticeRepository(
      db,
      deviceId: await meta.deviceId(),
      clock: clock,
    );
    final menuSettings = MenuSettingsRepository(meta);
    final audio = audioOverride ?? SoLoudAudioEngine();
    final referenceTone = await ReferenceToneController.load(audio, meta);
    return AppServices(
      practice: practice,
      menu: await PracticeMenuController.load(menuSettings, trumpetModes),
      dayConditions: DayConditionRepository(meta),
      audio: audio,
      metronome: await MetronomeController.load(audio, meta),
      referenceTone: referenceTone,
      tuner: TunerController(micOverride ?? RecordMicInput(), referenceTone),
      sync: SyncController(
        repository: practice,
        auth: authOverride,
        engine: remoteOverride == null
            ? null
            : SyncEngine(practice, remoteOverride),
        clock: clock,
      ),
      localAi: const UnavailableLocalAiService(),
      clock: clock,
    );
  }

  static Future<bool> _initFirebase() async {
    final options = DefaultFirebaseOptions.currentPlatform;
    if (options == null) return false;
    try {
      await Firebase.initializeApp(options: options);
      // 端末内のデータベースが正なので、Firestore 自身のオフライン保存は使わない
      FirebaseFirestore.instance.settings = const Settings(
        persistenceEnabled: false,
      );
      return true;
    } catch (e) {
      debugPrint('Firebase を使えないため、端末内だけで動かします: $e');
      return false;
    }
  }
}

/// 画面から [AppServices] を取り出すための入れ物
class AppScope extends InheritedWidget {
  const AppScope({super.key, required this.services, required super.child});

  final AppServices services;

  static AppServices of(BuildContext context) =>
      context.dependOnInheritedWidgetOfExactType<AppScope>()!.services;

  @override
  bool updateShouldNotify(AppScope oldWidget) => services != oldWidget.services;
}
