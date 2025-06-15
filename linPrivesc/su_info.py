from common_imports import *
from utils import print_error, skip

# Temporarily disabled due to long execution time
# @skip
# def find_suid_files(local_users):
#     root_suid_files = []
#     local_user_suid_files = []

#     try:
#         output = subprocess.check_output(["find", "/", "-perm", "-4000", "-type", "f"], stderr=subprocess.DEVNULL, universal_newlines=True)
#         for path in output.strip().split("\n"):
#             try:
#                 if not is_accessible(path, "x"):
#                     continue
#                 stat_info = os.stat(path)
#                 owner = pwd.getpwuid(stat_info.st_uid).pw_name
#                 if owner == "root":
#                     root_suid_files.append(path)
#                 elif owner in local_users:
#                     local_user_suid_files.append(path)
#             except Exception:
#                 continue
#     except Exception as e:
#         print_error("find_suid_files", e)

#     return root_suid_files, local_user_suid_files

@skip
def check_sudoers():
    print("[*] Checking sudo privileges (sudo -l):")
    try:
        output = subprocess.check_output(["sudo", "-l", "-n"], stderr=subprocess.STDOUT)
        print(output.decode())
    except subprocess.CalledProcessError as e:
        if b"a password is required" in e.output:
            print("  - sudo requires a password. Skipping further checks.")
        else:
            print_error("check_sudoers", e.output.decode())
    except Exception as e:
        print_error("check_sudoers", e)