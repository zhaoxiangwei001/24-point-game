[app]
title = 24点游戏
package.name = 二十四游戏
package.domain = org.example
source.dir = .
version = 0.1

[buildozer]
log_level = 2

# Android 配置
android.api = 33
android.minapi = 21
android.sdk = 27
android.ndk = 25b
android.allow_backup = true
android.arch = arm64-v8a

# 依赖项
requirements = python3,kivy
