#!/usr/bin/env python3

Remove API35-only android:defaultLocale for apktool compatibility

import sys, os, re
root = sys.argv[1] if len(sys.argv) > 1 else "."
p = os.path.join(root, "res/xml/_generated_res_locale_config.xml")
if os.path.exists(p):
    t = open(p, encoding="utf-8").read()
    t = re.sub("android:defaultLocale=" + chr(34) + "[^" + chr(34) + "]*" + chr(34), "", t)
    open(p, "w", encoding="utf-8").write(t)
    print("fixed", p)
