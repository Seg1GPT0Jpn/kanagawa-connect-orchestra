import 'package:flutter/material.dart';

import '../../../app/app_services.dart';
import '../../recording/presentation/recording_view.dart';
import 'metronome_view.dart';
import 'reference_tone_view.dart';
import 'tuner_view.dart';

/// 道具（チューナー・メトロノーム・基準音・録音）
class ToolsPage extends StatelessWidget {
  const ToolsPage({super.key});

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    final watch = Stopwatch()..start();
    return DefaultTabController(
      length: 4,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('道具'),
          bottom: const TabBar(
            // 4つの見出しが切れないように、横にスクロールできるようにする
            isScrollable: true,
            tabAlignment: TabAlignment.start,
            tabs: [
              Tab(text: 'チューナー'),
              Tab(text: 'メトロノーム'),
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
