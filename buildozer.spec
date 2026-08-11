[app]
title = Premium Door Lock
package.name = premiumdoorlock
package.domain = org.meuapp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1

requirements = python3,kivy==2.2.1,kivymd==1.1.1,plyer,pyjnius,pillow
android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET,USE_BIOMETRIC,USE_FINGERPRINT
android.api = 33
android.minapi = 21
android.ndk = 25b
android.enable_androidx = True
android.accept_sdk_license = True
android.archs = arm64-v8a
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1