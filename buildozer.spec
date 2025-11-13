[app]
title = 24点游戏
package.name = point24
package.domain = org.zxvdxt
source.dir = .
source.main = main.py
source.include_exts = py,png,jpg,kv
requirements = python3,kivy
version = 1.0
orientation = portrait

[buildozer]
log_level = 2

[android]
api = 28
minapi = 21
sdk = 20
ndk = 19c
permissions = INTERNET
android.accept_sdk_license = True

[ios]
[macos]
