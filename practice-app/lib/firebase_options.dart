// Firebase プロジェクト kco-practice の設定
//
// ここにある値はアプリを識別するためのもので、秘密情報ではありません（Web では誰でも見られます）。
// データを守っているのは Firestore のセキュリティルール（practice-app/firestore.rules）です。
//
// Android・iOS はまだ Firebase にアプリを登録していないので null（端末内だけで動く）。
// 登録したら `flutterfire configure` でこのファイルを作り直してください。
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

class DefaultFirebaseOptions {
  static FirebaseOptions? get currentPlatform => kIsWeb ? web : null;

  static const web = FirebaseOptions(
    apiKey: 'AIzaSyCzuJ4646K82qxuxrkQzPgv_YxWJjyXnjQ',
    authDomain: 'kco-practice.firebaseapp.com',
    projectId: 'kco-practice',
    storageBucket: 'kco-practice.firebasestorage.app',
    messagingSenderId: '448682739758',
    appId: '1:448682739758:web:fc63ea25e0f0856449f7bf',
  );
}
