import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/foundation.dart';

import 'auth_service.dart';

class FirebaseAuthService implements AuthService {
  FirebaseAuthService(this._auth);

  final FirebaseAuth _auth;

  static AppUser? _toAppUser(User? u) => u == null
      ? null
      : AppUser(uid: u.uid, email: u.email, displayName: u.displayName);

  @override
  AppUser? get currentUser => _toAppUser(_auth.currentUser);

  @override
  Stream<AppUser?> get userChanges => _auth.authStateChanges().map(_toAppUser);

  @override
  Future<void> signInWithGoogle() => _guard(() async {
    final provider = GoogleAuthProvider()
      ..setCustomParameters({'prompt': 'select_account'});
    if (kIsWeb) {
      await _auth.signInWithPopup(provider);
    } else {
      await _auth.signInWithProvider(provider);
    }
  });

  @override
  Future<void> signInWithEmail(String email, String password) => _guard(
    () => _auth.signInWithEmailAndPassword(
      email: email.trim(),
      password: password,
    ),
  );

  @override
  Future<void> signUpWithEmail(String email, String password) => _guard(
    () => _auth.createUserWithEmailAndPassword(
      email: email.trim(),
      password: password,
    ),
  );

  @override
  Future<void> sendPasswordReset(String email) =>
      _guard(() => _auth.sendPasswordResetEmail(email: email.trim()));

  @override
  Future<void> signOut() => _auth.signOut();

  static Future<void> _guard(Future<void> Function() action) async {
    try {
      await action();
    } on FirebaseAuthException catch (e) {
      throw AuthFailure(authErrorMessage(e.code));
    }
  }
}

/// Firebase Auth のエラーコード → 日本語の説明
String authErrorMessage(String code) => switch (code) {
  'invalid-email' => 'メールアドレスの形式が正しくありません',
  'user-disabled' => 'このアカウントは使えなくなっています',
  'user-not-found' ||
  'wrong-password' ||
  'invalid-credential' => 'メールアドレスかパスワードが違います',
  'email-already-in-use' => 'このメールアドレスはすでに登録されています',
  'weak-password' => 'パスワードは6文字以上にしてください',
  'operation-not-allowed' => 'このログイン方法は有効になっていません（運営に連絡してください）',
  'popup-closed-by-user' ||
  'cancelled-popup-request' ||
  'web-context-canceled' => 'ログインを中止しました',
  'popup-blocked' => 'ポップアップがブロックされました。ブラウザの設定で許可してください',
  'network-request-failed' => 'インターネットにつながっていません',
  'too-many-requests' => '試行回数が多すぎます。しばらくしてからお試しください',
  _ => 'ログインできませんでした（$code）',
};
