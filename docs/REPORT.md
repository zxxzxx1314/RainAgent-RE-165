# RainAgent 1.6.5 APK 逆向报告

## 一、目标
- 文件：RainAgent - 1.6.5.apk.1（62,222,813 B, md5 未变）
- 包名：com.agent.agoni；工程名 Z-Agent（cn.rain.zagent）
- 构建：AGP 9.2.1 / Chaquopy 16.1.0 / Python 3.12

## 二、结构
| 组件 | 说明 |
|---|---|
| classes.dex (8.0 MB) | 主程序：androlua + luajava + lua55 + UI/插件 |
| assets/mao.dex | AXML/ARSC 解析器（ARSCDecoder/AXmlDecoder/StringBlock） |
| assets/sign.dex | APK 签名器（assets/keys/ 下 keystore/pk8/sbt/x509） |
| assets/secure/rain.enc | 加密核心 dex（16,844 B） |
| lib/arm64-v8a/libseal.so | 解密密钥提供者（4,440 B） |
| assets/linux/* | proot 环境（bootstrap-aarch64.zip 32.8 MB） |
| assets/lua_template.apk | 打包用 Lua 模板 |

## 三、解密链（完整还原）

SensitiveLoader.b():
 read assets/secure/rain.enc
 iv = body[0:12]
 ct = body[12:] (密文+tag)
 cipher = AES/GCM/NoPadding
 key = SealKey.key() -> nativeKey() [libseal.so]
 spec = GCMParameterSpec(128, iv)
 pt = cipher.doFinal(...)
 InMemoryDexClassLoader(pt, parent)


## 四、nativeKey 算法
libseal.so（arm64, 无符号表）.text 仅 292 B，.rodata 48 B。
asm
; 循环 i=0..31:
; w13 = A[i] (rodata 0x528)
; w12 = B[i & 0xf] (rodata 0x548)
; out[i] = w12 ^ w13

常量（明文）：

A = e0607d793957c8b4f94d28e4db39b9a648bab8fde66d1abdf91963d3e97186c0
B = 50983b2b52c064b7c6da327390a1d562
key[i] = A[i] XOR B[i & 0xf]
=> AES-256 key = b0f846526b97ac033f971a974b986cc4182283d6b4ad7e0a3fc351a079d053a2


## 五、解密产物（rain.dex 16,816 B）
| 类 | 作用 |
|---|---|
| NetAuthReal | 鉴权 + 拉取远程配置（fetchConfig/verify/post/androidId/deviceCode） |
| NetGuardReal | 设备码守卫 + 网络回调 |
| NetStore | 本地存储 |
| NetAuthImpl / NetGuardImpl | 接口 |

### 网络协议

POST https://agoni.xn--rhyr4ib67a.top/RainAgent/api.php
APP_ID = APP09EC7766A1CD
Content-Type: application/json; charset=utf-8
字段: app_id, device_code, android_id, key, url, json
device_code = MD5(android_id) hex(%02x)


## 六、产物清单
- artifacts/rain_decrypted.dex 解密后的核心 dex
- artifacts/rain.enc 加密原包
- artifacts/libseal.so 密钥 so
- artifacts/classes.dex / mao.dex / sign.dex 其余 dex
- artifacts/AndroidManifest.xml
- docs/rain_dex_strings.txt 解密 dex 全部字符串
- scripts/decrypt.py 可复现解密脚本