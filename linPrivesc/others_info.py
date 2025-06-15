from common_imports import *
from constants import KEYWORDS, DIRS, EXTS, CURRENT_USER
from utils import is_accessible, print_error, skip

@skip
def check_basic():
    print(f"[*] Hostname: {socket.gethostname()}")
    print(f"[*] OS: {platform.system()}")
    print(f"[*] Kernel version: {platform.release()}")
    print(f"[*] Architecture: {platform.machine()}")

@skip
def find_keywords():
    print("[*] Searching for other suspicious files...\n")

    keyword_pattern = re.compile("|".join(KEYWORDS), re.IGNORECASE)
    matched_lines = []
    suspicious_files = []
    target_exts = EXTS
    special_filenames = [".htaccess", ".htpasswd"]

    for base_dir in DIRS:
        for root, dirs, files in os.walk(base_dir):
            for fname in files:
                full_path = os.path.join(root, fname)

                try:
                    if not is_accessible(full_path, "r"):
                        continue

                    if fname.lower().split(".")[-1] in target_exts:
                        suspicious_files.append(full_path)

                    if fname in special_filenames:
                        suspicious_files.append(full_path)

                    if not is_accessible(full_path, "r"):
                        continue

                    with open(full_path, "r", errors="ignore") as f:
                        for i, line in enumerate(f):
                            if keyword_pattern.search(line):
                                matched_lines.append((full_path, i+1, line.strip()))
                                break
                except Exception:
                    continue

    if matched_lines:
        print("[!] Keyword matches in file contents:")
        for path, lineno, line in matched_lines:
            print(f"  - {path} (line {lineno}): {line}")
    else:
        print("  - No keyword matches found in file contents.")

    if suspicious_files:
        print("\n[!] Suspicious files based on extension or filename:")
        for f in suspicious_files:
            print(f"  - {f}")
    else:
        print("\n  - No suspicious files found by extension or filename.")

@skip
def check_ports():
    print("[*] Checking open ports and listening processes (ss -tulnp)...")
    try:
        output = subprocess.check_output(["ss", "-tulnp"], stderr=subprocess.STDOUT, text=True)
        lines = output.strip().split("\n")

        if len(lines) < 2:
            print("  - No listening ports found.")
            return

        print("\nProto    Local Address      PID/Program")
        print("-------------------------------------------")
        for line in lines[1:]:
            parts = line.split()
            if len(parts) < 6 or "users:" not in line:
                continue

            proto = parts[0]
            local_addr = parts[4]
            users_info = " ".join(parts[6:])

            match = re.search(r'users:\(\("([^"]+)",pid=(\d+),', users_info)
            if match:
                proc_name, pid = match.groups()
                proc_info = f"{pid}/{proc_name}"
            else:
                proc_info = "unknown"

            print(f"{proto:<8} {local_addr:<18} {proc_info}")

    except subprocess.CalledProcessError as e:
        print_error("check_ports", e.output)
    except Exception as e:
        print_error("check_ports", e)

@skip
def check_processes(local_users):
    print("[*] Checking running processes (ps aux)...")
    try:
        output = subprocess.check_output(["ps", "aux"], universal_newlines=True)
        lines = output.strip().split("\n")
        headers = lines[0]
        processes = lines[1:]

        root_processes = []
        local_users_processes = []
        current_user_processes = []

        for line in processes:
            cols = line.split()
            if len(cols) < 11:
                continue
            user = cols[0]
            cmd = " ".join(cols[10:])

            if user == "root":
                root_processes.append(cmd)
            elif user == CURRENT_USER:
                current_user_processes.append(cmd)
            elif user in local_users:
                local_users_processes.append(f"{user}: {cmd}")

        print("\n[*] Processes run by root:")
        for cmd in root_processes:
            print(f"  - {cmd}")

        print("\n[*] Processes run by current user:")
        for cmd in current_user_processes:
            print(f"  - {cmd}")

        print("\n[*] Processes run by other local users:")
        for cmd in local_users_processes:
            print(f"  - {cmd}")
    except Exception as e:
        print_error("check_processes", e)