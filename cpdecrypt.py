import sys
from Crypto.Cipher import AES
from base64 import b64decode

NUM = 70
KEY_HEX = """
4e 99 06 e8 fc b6 6c c9 fa f4 93 10 62 0f fe e8
f4 96 e8 06 cc 05 79 90 20 9b 09 a4 33 b6 6c 1b
"""
IV = b"\x00" * 16

def get_key_from_hex(key_hex):
    return bytes.fromhex("".join(key_hex.split()))

def unpad_pkcs7(data):
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 16:
        raise ValueError("INVALID PADDING LENGTH")
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("INVALID PADDING BYTES")
    return data[:-pad_len]

def main():
    try:
        print("\n" + "=" * NUM)
        print(r"""
___________________________                                      __   
\_   ___ \______   \______ \   ____   ___________ ___.__._______/  |_ 
/    \  \/|     ___/|    |  \_/ __ \_/ ___\_  __ <   |  |\____ \   __\
\     \___|    |    |    `   \  ___/\  \___|  | \/\___  ||  |_> >  |  
 \______  /____|   /_______  /\___  >\___  >__|   / ____||   __/|__|  
        \/                 \/     \/     \/       \/     |__|                                      
        """)
        print("=" * NUM + "\n")

        cpassword = input("CPASSWORD:\n> ").strip()
        key = get_key_from_hex(KEY_HEX)
        password_bytes = b64decode(cpassword, validate=True)
        cipher = AES.new(key, AES.MODE_CBC, IV)
        decrypted = cipher.decrypt(password_bytes)

        try:
            unpadded = unpad_pkcs7(decrypted)
            password_utf16 = unpadded.decode('utf-16le')
            print(f"\n[+] DECRYPTED PASSWORD:\n{password_utf16}\n")
        except Exception as e:
            print(f"[!] PADDING OR DECODING ERROR: {e}")
            return 1

        return 0

    except KeyboardInterrupt:
        print("\n[!] INTERRUPTED BY USER. EXITING...")
        return 1
    except Exception as e:
        print(f"\n[x] UNEXPECTED ERROR: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
