import sys
from Crypto.Cipher import AES
from base64 import b64decode

NUM = 90
KEY_HEX = """
4e 99 06 e8 fc b6 6c c9 fa f4 93 10 62 0f fe e8
f4 96 e8 06 cc 05 79 90 20 9b 09 a4 33 b6 6c 1b
"""
IV = b"\x00" * 16

def get_key_from_hex(key_hex):
    return bytes.fromhex("".join(key_hex.split()))

def main():
    try:
        print("\n" + "=" * NUM)
        print(r"""
___________________  _____    _________ _________ ________  ___________________________________.___._____________________
\_   ___ \______   \/  _  \  /   _____//   _____/ \______ \ \_   _____/\_   ___ \______   \__  |   |\______   \__    ___/
/    \  \/|     ___/  /_\  \ \_____  \ \_____  \   |    |  \ |    __)_ /    \  \/|       _//   |   | |     ___/ |    |   
\     \___|    |  /    |    \/        \/        \  |    `   \|        \\     \___|    |   \\____   | |    |     |    |   
 \______  /____|  \____|__  /_______  /_______  / /_______  /_______  / \______  /____|_  // ______| |____|     |____|   
        \/                \/        \/        \/          \/        \/         \/       \/ \/                            
        """)
        print("=" * NUM + "\n")

        cpassword = input("CPASSWORD:\n> ").strip()
        key = get_key_from_hex(KEY_HEX)

        password = b64decode(cpassword, validate=True)

        cipher = AES.new(key, AES.MODE_CBC, IV)
        decrypted = cipher.decrypt(password)

        try:
            pad_len = decrypted[-1]
            if pad_len < 1 or pad_len > 16:
                raise ValueError("Invalid padding length")
            password_utf16 = decrypted[:-pad_len]
            print(password_utf16.decode('utf-16'))
        except Exception as e:
            print(f"[!] パディングまたはデコードエラー: {e}")
            return 1
        return 0
    
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Exiting...")
        return 1
    
    except Exception as e:
        print(f"\n[x] Unexpected error occurred: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())