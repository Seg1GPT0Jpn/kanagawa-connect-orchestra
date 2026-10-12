import 'package:flutter/material.dart';

import '../../../app/app_services.dart';
import '../../recording/presentation/recording_view.dart';
import 'click_track_view.dart';
import 'metronome_view.dart';
import 'reference_tone_view.dart';
import 'sound_settings_sheet.dart';
import 'tuner_view.dart';

/// 道具（チューナー・メトロノーム・クリックトラック・基準音・録音）
class ToolsPage extends StatelessWidget {
  const ToolsPage({super.key});

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    final watch = Stopwatch()..start();
    return DefaultTabController(
      length: 5,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('道具'),
          actions: [
            IconButton(
              tooltip: '音の設定・テスト',
              onPressed: () => SoundSettingsSheet.show(context, services.mixer),
              icon: const Icon(Icons.volume_up_outlined),
            ),
          ],
          bottom: const TabBar(
            // 4つの見出しが切れないように、横にスクロールできるようにする
            isScrollable: true,
            tabAlignment: TabAlignment.start,
            tabs: [
              Tab(text: 'チューナー'),
              Tab(text: 'メトロノーム'),
              Tab(text: 'クリックトラック'),
              Tab(text: '基準音'),
              Tab(text: '録音'),
            ],
          ),
        ),
        body: TabBarView(
          children: [
            TunerView(
              controller: services.tuner,
              pitch: services.referenceTone,
            ),
            MetronomeView(
              controller: services.metronome,
              clock: () => watch.elapsed,
            ),
            ClickTrackView(controller: services.clickTrack),
            ReferenceToneView(controller: services.referenceTone),
            RecordingView(
              controller: services.recording,
              pitch: services.referenceTone,
            ),
          ],
        ),
      ),
    );
  }
}
