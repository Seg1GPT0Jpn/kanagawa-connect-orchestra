import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/local_ai/local_ai_service.dart';

void main() {
  test('AI が使えないときの実装は isSupported=false で、呼ぶと LocalAiException', () async {
    const LocalAiService ai = UnavailableLocalAiService();
    expect(ai.isSupported, isFalse);
    await expectLater(ai.initializeModel(), throwsA(isA<LocalAiException>()));
    await expectLater(
      ai.generatePrompt('hi'),
      throwsA(isA<LocalAiException>()),
    );
  });
}
