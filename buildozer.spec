
[app]
title = WiFi Security
package.name = wifisecurity
package.domain = org.example

source.dir = .
source.include_exts = py,kv,txt
version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.api = 35
android.minapi = 23
android.archs = arm64-v8a
android.private_storage = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
