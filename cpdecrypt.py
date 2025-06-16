#!/usr/bin/env python3

import base64
from Crypto.Cipher import AES

IV = b"\x00" * 16
KEY_HEX = "0123456789abcdef0123456789abcdef"

def info(msg):
    print(f"\033[94m[*] {msg}\033[0m")

def warn(msg):
    print(f"\033[91m[-] {msg}\033[0m")

def ok(msg):
    print(f"\033[92m[+] {msg}\033[0m")

def pkcs7_unpad(data):
    pad_len = data[-1]
    if pad_len < 1 or pad_len > AES.block_size:
        raise ValueError("Invalid padding length.")
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Invalid padding bytes.")
    return data[:-pad_len]

def decrypt_aes_cbc(base64_ciphertext, key_hex):
    key = bytes.fromhex(key_hex)
    ciphertext = base64.b64decode(base64_ciphertext)
    cipher = AES.new(key, AES.MODE_CBC, IV)
    decrypted = cipher.decrypt(ciphertext)
    unpadded = pkcs7_unpad(decrypted)
    return unpadded.decode("utf-16le")

if __name__ == "__main__":
    info("AES-CBC decoder for Python 3.5")
    info(f"KEY (hex): {KEY_HEX}")
    info("IV is 16 null bytes (\\x00 * 16)")

    try:
        b64input = input("Input base64 ciphertext:\n> ").strip()
        result = decrypt_aes_cbc(b64input, KEY_HEX)
        ok("Decryption success:")
        print(result)
    except Exception as e:
        warn(f"Decryption failed: {e}")
