#!/usr/bin/env python3

Fix apktool-produced resource names starting with $ (AVD intermediates)

import os, sys
D = chr(36)
root = sys.argv[1] if len(sys.argv) > 1 else "."
n1 = n2 = 0
for r, ds, fs in os.walk(os.path.join(root, "res")):
    for f in fs:
        if f.startswith(D):
            src = os.path.join(r, f)
            dst = os.path.join(r, f[1:])
            if not os.path.exists(dst):
                os.rename(src, dst); n1 += 1
for r, ds, fs in os.walk(os.path.join(root, "res")):
    for f in fs:
        if not f.endswith(".xml"): continue
        p = os.path.join(r, f)
        t = open(p, encoding="utf-8", errors="replace").read()
        n = t.replace("@drawable/" + D, "@drawable/").replace("@anim/" + D, "@anim/")
        if n != t:
            open(p, "w", encoding="utf-8").write(n); n2 += 1
pub = os.path.join(root, "res/values/public.xml")
if os.path.exists(pub):
    t = open(pub, encoding="utf-8", errors="replace").read()
    open(pub, "w", encoding="utf-8").write(t.replace("name=" + chr(34) + D, "name=" + chr(34)))
print("renamed", n1, "ref-fixed", n2)
