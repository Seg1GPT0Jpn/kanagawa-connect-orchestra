import 'package:flutter/material.dart';

import '../../../app/app_services.dart';
import 'metronome_view.dart';
import 'reference_tone_view.dart';

/// 道具（メトロノーム・基準音・チューナー）
class ToolsPage extends StatelessWidget {
  const ToolsPage({super.key});

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    final watch = Stopwatch()..start();
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('道具'),
          bottom: const TabBar(
            tabs: [
              Tab(text: 'メトロノーム'),
              Tab(text: '基準音'),
            ],
          ),
        ),
        body: TabBarView(
          children: [
            MetronomeView(
              controller: services.metronome,
              clock: () => watch.elapsed,
            ),
            ReferenceToneView(controller: services.referenceTone),
          ],
        ),
      ),
    );
  }
}
