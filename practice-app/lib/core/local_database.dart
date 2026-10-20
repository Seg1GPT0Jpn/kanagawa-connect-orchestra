/// 端末内のデータベース（Web はブラウザの IndexedDB、Android・iOS はアプリ内のファイル）
library;

export 'local_database_io.dart'
    if (dart.library.js_interop) 'local_database_web.dart';
