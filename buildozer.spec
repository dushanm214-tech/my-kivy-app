[app]
title = Apparel Planner
package.name = apparelplanner
package.domain = org.factory

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0.0

requirements = python3,kivy==2.3.0,kivymd==1.2.0

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.api = 33
android.minapi = 26
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
