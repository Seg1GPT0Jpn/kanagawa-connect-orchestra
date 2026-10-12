/// ログイン（クラウド同期のため。ログインしなくてもアプリは使える）
library;

class AppUser {
  const AppUser({required this.uid, this.email, this.displayName});

  final String uid;
  final String? email;
  final String? displayName;
}

class AuthFailure implements Exception {
  const AuthFailure(this.message);

  /// 画面に出す説明（日本語）
  final String message;

  @override
  String toString() => message;
}

abstract interface class AuthService {
  AppUser? get currentUser;
  Stream<AppUser?> get userChanges;
  Future<void> signInWithGoogle();
  Future<void> signInWithEmail(String email, String password);
  Future<void> signUpWithEmail(String email, String password);
  Future<void> sendPasswordReset(String email);
  Future<void> signOut();
}
