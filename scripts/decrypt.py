#!/usr/bin/env python3
# RainAgent 1.6.5 encrypted-dex decryptor (reproducible)
# usage: python3 decrypt.py rain.enc out.dex | deps: pip install pycryptodome
import sys
from Crypto.Cipher import AES
A = bytes.fromhex('e0607d793957c8b4f94d28e4db39b9a648bab8fde66d1abdf91963d3e97186c0')
B = bytes.fromhex('50983b2b52c064b7c6da327390a1d562')
def native_key():
	return bytes(A[i] ^ B[i & 0xf] for i in range(32))
def main(enc, out):
	d = open(enc, 'rb').read()
	iv, body = d[:12], d[12:]
	key = native_key()
	c = AES.new(key, AES.MODE_GCM, nonce=iv, mac_len=16)
	pt = c.decrypt_and_verify(body[:-16], body[-16:])
	open(out, 'wb').write(pt)
	print('key =', key.hex())
	print('out =', out, len(pt), 'bytes')
if name == 'main':
	main(sys.argv[1], sys.argv[2])