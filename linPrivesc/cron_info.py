from common_imports import *
from utils import is_accessible, print_error, skip

@skip
def check_cron():
    print("[*] Checking cron jobs...\n")
    # check_crontab()
    # check_crond()
    check_user_crontab()

@skip
def parse_cron(path):
    jobs = []
    try:
        if not is_accessible(path, "r"):
            return []
        with open(path, "r") as file:
            for line in file:
                if line.strip() and not line.startswith("#"):
                    jobs.append(line.strip())
    except Exception as e:
        print_error(f"parse_crontab_file: {path}", e)
    return jobs

# @skip
# def check_crontab():
#     print("[*] /etc/crontab:")
#     jobs = parse_cron("/etc/crontab")
#     for job in jobs:
#         print(f"  - {job}")

# @skip
# def check_crond():
#     print("\n[*] Files in /etc/cron.d/:")
#     if os.path.isdir("/etc/cron.d/"):
#         for fname in os.listdir("/etc/cron.d/"):
#             path = os.path.join("/etc/cron.d/", fname)
#             print(f"  - {path}")
#             jobs = parse_cron(path)
#             for job in jobs:
#                 print(f"    > {job}")

@skip
def check_user_crontab():
    print("\n[*] User crontab (crontab -l):")
    try:
        output = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT)
        for line in output.decode().splitlines():
            if line.strip() and not line.startswith("#"):
                print(f"  - {line.strip()}")
    except subprocess.CalledProcessError as e:
        if b'no crontab for' in e.output:
            print("  - (No crontab for user)")
        else:
            print_error("check_user_crontab", e)
    except Exception as e:
        print_error("check_user_crontab", e)