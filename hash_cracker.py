import sys
import os
import subprocess
import re

def info(msg):
    print("\033[94m[*] {}\033[0m".format(msg))

def warn(msg):
    print("\033[91m[-] {}\033[0m".format(msg))

def ok(msg):
    print("\033[92m[+] {}\033[0m".format(msg))

WORDLIST_PATH = "/usr/share/wordlists/rockyou.txt"
NUM = 90

HASH_PATTERNS = {
    "MD5": r"^[a-fA-F0-9]{32}$",
    "NTLM": r"^[a-fA-F0-9]{32}$",
    "MD5crypt": r"^\$1\$[a-fA-F0-9]{32}$",
    "SHA-1": r"^[a-fA-F0-9]{40}$",
    "SHA-256": r"^[a-fA-F0-9]{64}$",
    "SHA-512": r"^[a-fA-F0-9]{128}$",
    "SHA-256crypt": r"^\$5\$.*",
    "SHA-512crypt": r"^\$6\$.*",
    "bcrypt": r"^\$2[aby]?\$\d{2}\$.{53}$",
    "NetNTLMv1": r"^[a-fA-F0-9]{32}:[a-fA-F0-9]{32}$",
    "NetNTLMv2": r"^[a-fA-F0-9]{32}:[a-fA-F0-9]{32}:[a-fA-F0-9]{16,}:.+",
    "Kerberos 5 TGS": r"^\$krb5tgs\$.*",
}

JOHN_FORMAT = {
    "MD5": "raw-md5",
    "NTLM": "nt",
    "MD5crypt": "md5crypt",
    "SHA-1": "raw-sha1",
    "SHA-256": "raw-sha256",
    "SHA-512": "raw-sha512",
    "SHA-256crypt": "sha256crypt",
    "SHA-512crypt": "sha512crypt",
    "bcrypt": "bcrypt",
    "NetNTLMv1": "netntlm",
    "NetNTLMv2": "netntlmv2",
    "Kerberos 5 TGS": "krb5tgs",
}

def select_mode():
    info("MODE:")
    print("1: ANALYZE HASH TYPE")
    print("2: ANALYZE HASH TYPE AND CRACK IT")
    return input("> ").strip()

def analyze_hash_type(hash_input):
    candidates = []
    for name, pattern in HASH_PATTERNS.items():
        if re.fullmatch(pattern, hash_input):
            candidates.append(name)
    return candidates

def select_from_candidates(candidates):
    info("MULTIPLE POSSIBLE HASH TYPES DETECTED:")
    for i, name in enumerate(candidates, 1):
        print("{}: {}".format(i, name))
    while True:
        selected = input("SELECT THE HASH TYPE:\n> ").strip()
        if selected.isdigit() and 1 <= int(selected) <= len(candidates):
            return candidates[int(selected) - 1]
        warn("INVALID CHOICE. TRY AGAIN.")

def check_rockyou():
    rockyou_path = WORDLIST_PATH
    rockyou_gz_path = rockyou_path + ".gz"
    if os.path.exists(rockyou_path):
        return rockyou_path
    elif os.path.exists(rockyou_gz_path):
        warn("PLEASE EXTRACT rockyou.txt.gz AT {}".format(rockyou_gz_path))
        return None
    else:
        warn("rockyou.txt OR rockyou.txt.gz NOT FOUND.")
        return None

def crack(hash_input, hash_type, wordlist):
    chosen_format = JOHN_FORMAT.get(hash_type)
    if not chosen_format:
        warn("UNSUPPORTED HASH FORMAT FOR CRACKING.")
        return 1

    tmp_hash_file = "hash.txt"
    with open(tmp_hash_file, "w") as f:
        f.write(hash_input + "\n")

    info("CRACKING HASH USING FORMAT: {}".format(chosen_format))
    print("=" * NUM)

    try:
        result = subprocess.run([
            "john",
            "--format={}".format(chosen_format),
            "--wordlist={}".format(wordlist),
            "--fork=4",
            tmp_hash_file
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        if result.returncode != 0:
            warn("John error:\n{}".format(result.stderr))
            return 1

        show_output = subprocess.check_output(
            ["john", "--show", "--format={}".format(chosen_format), tmp_hash_file],
            universal_newlines=True).strip()
        print(show_output)
        print("=" * NUM)

        for line in show_output.splitlines():
            if ":" in line:
                parts = line.split(":")
                if len(parts) >= 2:
                    password = parts[1]
                    ok("PASSWORD FOUND: {}".format(password))
                    return 0

        warn("PASSWORD NOT FOUND IN --show output.")
        return 1

    except Exception as e:
        warn("CRACKING FAILED: {}".format(e))
        return 1

    finally:
        if os.path.exists(tmp_hash_file):
            os.remove(tmp_hash_file)

def main():
    try:
        print("\n" + "=" * NUM)
        print(r"""
      ___ ___               .__      _________                       __                 
     /   |   \_____    _____|  |__   \_   ___ \____________    ____ |  | __ ___________ 
    /    ~    \__  \  /  ___/  |  \  /    \  \/\_  __ \__  \ _/ ___\|  |/ // __ \_  __ \
    \    Y    // __ \_\___ \|   Y  \ \     \____|  | \// __ \\  \___|    <\  ___/|  | \/
     \___|_  /(____  /____  >___|  /  \______  /|__|  (____  /\___  >__|_ \\___  >__|   
          \/      \/     \/     \/          \/            \/     \/     \/    \/       
        """)
        print("=" * NUM + "\n")

        mode = select_mode()
        if mode not in ("1", "2"):
            warn("INVALID MODE. EXITING...")
            return 1

        hash_input = input("Enter a hash:\n> ").strip()
        if not hash_input:
            warn("NO HASH. EXITING...")
            return 1

        candidates = analyze_hash_type(hash_input)
        if not candidates:
            warn("UNKNOWN HASH. EXITING...")
            return 1

        if mode == "1":
            info("POSSIBLE HASH TYPES FOUND:")
            for name in candidates:
                print("- {}".format(name))
            return 0

        if mode == "2":
            if len(candidates) == 1:
                selected_type = candidates[0]
            else:
                selected_type = select_from_candidates(candidates)

            ok("SELECTED HASH TYPE: {}".format(selected_type))
            wordlist = check_rockyou()
            if not wordlist:
                warn("rockyou.txt NOT FOUND. EXITING...")
                return 1

            return crack(hash_input, selected_type, wordlist)

        return 0

    except KeyboardInterrupt:
        warn("INTERRUPTED BY USER. EXITING...")
        return 1

    except Exception as e:
        warn("UNEXPECTED ERROR OCCURRED: {}".format(e))
        return 1

if __name__ == '__main__':
    sys.exit(main())
