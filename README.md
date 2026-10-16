# RainAgent 1.6.5 · APK 逆向 + 重编译工程

对 RainAgent - 1.6.5.apk（com.agent.agoni）做完整静态逆向，并把加密内核解密、
资源修正后重新编译成可安装 APK。

#H@ 一、成果

项目	状态
加密 dex 解密	完成
native 密钥算法还原	完成（libseal.so）
反编译（smali + res + assets）	完成（apktool 2.9.3）
重新编译	成功
签名（v1+v2+v3）	成功

#H@ 二、加密链

assets/secure/rain.enc（16,844 B）= iv(12) + AES-256-GCM 密文 + tag(16)

密钥来自 lib/arm64-v8a/libseal.so 的 Java_..._SealKey_nativeKey：

text
复制
下载
key[i] = A[i] XOR B[i & 0xf]     (i = 0..31)

A = e0607d793957c8b4f94d28e4db39b9a648bab8fde66d1abdf91963d3e97186c0
B = 50983b2b52c064b7c6da327390a1d562
=> AES-256 key = b0f846526b97ac033f971a974b986cc4182283d6b4ad7e0a3fc351a079d053a2

解密后得到 rain.dex（16,816 B），含 NetAuthReal / NetGuardReal / NetStore。
网络端点：https://agoni.xn--rhyr4ib67a.top/RainAgent/api.php，APP_ID=APP09EC7766A1CD。

#H@ 三、目录

text
复制
下载
artifacts/   解密产物与原 dex（rain.decrypted.dex / libseal.so / mao.dex / sign.dex ...）
docs/        REPORT.md（完整报告）、rain_dex_strings.txt
scripts/     decrypt.py（可复现解密）
rebuilt/     rebuild.sh + fix_*.py + rain.keystore（重编译流水线）

#H@ 四、重编译（Termux）

text
复制
下载
pkg install openjdk-17 aapt2
# 需自备 apktool.jar / uber-apk-signer.jar 到 $TERMUX_PREFIX/bin
cd rebuilt && bash rebuild.sh <原始APK> [工作目录] [输出APK]

关键修复点（apktool 2.9.3 已知缺陷）：

aapt2 自带 glibc 版在 Android 上 SIGILL → 改用系统 aapt2（$(command -v aapt2)）

40 个以 $ 开头的 AVD 中间资源名被 aapt2 拒绝 → 去前缀并同步改引用 + public.xml

_generated_res_locale_config.xml 的 android:defaultLocale（API35）→ 删除

#H@ 五、重建 APK

产物体积 59.5 MiB（原 59.3 MiB），assets/、lib/、rain.enc 逐字节一致；
差异仅为 apktool 还原资源语义名（原 APK 资源名被混淆为 res/-1.xml）。

下载：见 GitHub Releases。

#H@ 六、许可与声明

本仓库仅为互操作 / 安全研究用途，内容为逆向分析产物。原始软件版权归其作者所有。
