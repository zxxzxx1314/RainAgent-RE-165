#!/data/data/com.termux/files/usr/bin/bash
# RainAgent 1.6.5 rebuild pipeline (Termux)
# deps: pkg install openjdk-17 aapt2 ; plus apktool.jar, uber-apk-signer.jar
set -e
APK="$1"
WORK="${2:-./work}"
OUT="${3:-./rebuilt.apk}"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$WORK"
echo "[1/5] apktool decode"
apktool d -f -o "$WORK/decompiled" "$APK"
echo "[2/5] fix dollar-prefixed resources"
python3 "$HERE/fix_dollar_resources.py" "$WORK/decompiled"
echo "[3/5] fix API35 locale attr"
python3 "$HERE/fix_locale_config.py" "$WORK/decompiled"
echo "[4/5] rebuild with system aapt2"
apktool b --use-aapt2 --aapt "$(command -v aapt2)" -o "$WORK/rebuilt.apk" "$WORK/decompiled"
echo "[5/5] sign v1+v2+v3"
java -jar "$TERMUX_PREFIX/bin/uber-apk-signer.jar" --apks "$WORK/rebuilt.apk" --ks "$HERE/rain.keystore" --ksAlias rain --ksPass rain123456 --ksKeyPass rain123456 --allowResign --skipZipAlign -o "$(dirname "$OUT")"
echo done
