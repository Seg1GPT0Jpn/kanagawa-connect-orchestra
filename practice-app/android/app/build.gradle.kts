import java.io.FileInputStream
import java.util.Properties

plugins {
    id("com.android.application")
    // The Flutter Gradle Plugin must be applied after the Android and Kotlin Gradle plugins.
    id("dev.flutter.flutter-gradle-plugin")
}

// リリース用の署名の鍵（android/key.properties。リポジトリには入れない。手順は docs/release.md）
// 鍵がないままリリース版を作ろうとすると、ビルドを失敗させる（誤った署名のアプリを
// 公開候補にしてしまう事故を防ぐ）。デバッグ版のビルドには鍵はいらない。
// 手元でリリース版の動きだけ確かめたいときは、環境変数 KCO_ALLOW_DEBUG_SIGNED_RELEASE=1 を
// 付けるとデバッグ用の鍵で署名する（この APK は公開に使えない）。
val keystorePropertiesFile = rootProject.file("key.properties")
val keystoreProperties = Properties().apply {
    if (keystorePropertiesFile.exists()) FileInputStream(keystorePropertiesFile).use { load(it) }
}
val requiredKeys = listOf("keyAlias", "keyPassword", "storeFile", "storePassword")
val missingKeys = requiredKeys.filter { keystoreProperties.getProperty(it).isNullOrBlank() }
val hasReleaseKey = keystorePropertiesFile.exists() && missingKeys.isEmpty() &&
    file(keystoreProperties.getProperty("storeFile")).exists()
val allowDebugSignedRelease = System.getenv("KCO_ALLOW_DEBUG_SIGNED_RELEASE") == "1"

android {
    namespace = "jp.kanagawaconnect.kco_practice"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    defaultConfig {
        // ストアに登録するアプリの ID（一度公開したら変えられない）
        applicationId = "jp.kanagawaconnect.kco_practice"
        // You can update the following values to match your application needs.
        // For more information, see: https://flutter.dev/to/review-gradle-config.
        // 端末内 AI（Gemini Nano・ML Kit GenAI）の部品が Android 8.0（API 26）以上を求める
        minSdk = 26
        targetSdk = flutter.targetSdkVersion
        // Uses the version code from pubspec.yaml. When using split APKs, 1000 * ABI_VERSION
        // is added automatically by Flutter. (https://developer.android.com/studio/build/configure-apk-splits#configure-APK-versions)
        // You can force using the value of versionCode by specifying the `-P force-version-code-ignoring-abi=true`
        // flag during build.
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }

    signingConfigs {
        if (hasReleaseKey) {
            create("release") {
                keyAlias = keystoreProperties["keyAlias"] as String
                keyPassword = keystoreProperties["keyPassword"] as String
                storeFile = file(keystoreProperties["storeFile"] as String)
                storePassword = keystoreProperties["storePassword"] as String
            }
        }
    }

    buildTypes {
        release {
            signingConfig = when {
                hasReleaseKey -> signingConfigs.getByName("release")
                allowDebugSignedRelease -> signingConfigs.getByName("debug")
                else -> null
            }
        }
    }
}

// リリース版（APK・App Bundle）を作るときだけ、鍵があるかを確かめる
gradle.taskGraph.whenReady {
    val buildsRelease = allTasks.any { t ->
        t.project == project && t.name.contains("Release") &&
            (t.name.startsWith("assemble") || t.name.startsWith("bundle") ||
                t.name.startsWith("package"))
    }
    if (buildsRelease && !hasReleaseKey && !allowDebugSignedRelease) {
        val reason = when {
            !keystorePropertiesFile.exists() -> "android/key.properties がありません"
            missingKeys.isNotEmpty() -> "android/key.properties に ${missingKeys.joinToString()} がありません"
            else -> "鍵のファイル（storeFile）が見つかりません"
        }
        throw GradleException(
            "リリース版には公開用の署名の鍵が必要です（$reason）。手順は practice-app/docs/release.md。" +
                "動作の確認だけなら、環境変数 KCO_ALLOW_DEBUG_SIGNED_RELEASE=1 を付けてください（公開には使えません）"
        )
    }
}

kotlin {
    compilerOptions {
        jvmTarget = org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17
    }
}

flutter {
    source = "../.."
}
