from common_imports import *
from constants import CURRENT_USER
from utils import skip
from su_info import find_suid_files

@skip
def check_user(local_users):
    groups = get_user_groups(CURRENT_USER)
    print(f"[*] Current user: {CURRENT_USER}")
    print(f"[*] Groups: {', '.join(groups)}")

    # Temporarily disabled due to long execution time
    # group_exec_files = find_group_files(groups)
    # print("[*] Executable files accessible by current user's groups:")
    # for file in group_exec_files:
    #     print(f"  - {file}")

    root_suid_files, local_user_suid_files = find_suid_files(local_users)
    print(f"[*] SUID files owned by root:")
    for file in root_suid_files:
        print(f"  - {file}")
    print("[*] SUID files owned by local users:")
    for file in local_user_suid_files:
        print(f"  - {file}")

@skip
def get_users():
    print(f"[*] Current user: {CURRENT_USER}")
    
    local_users = []
    print(f"[*] Local users found in /etc/passwd:")
    for user in pwd.getpwall():
        if int(user.pw_uid) >= 1000 and "home" in user.pw_dir:
            print(f"    - {user.pw_name}")
            local_users.append(user.pw_name)

    return local_users

@skip
def get_user_groups(user):
    groups = []
    gids = os.getgrouplist(user, os.getgid())
    for gid in gids:
        groups.append(grp.getgrgid(gid).gr_name)
    return groups

# Temporarily disabled due to long execution time; under optimization.
# @skip
# def find_group_files(groups):
#     group_exec_files = []
#     group_gids = [g.gr_gid for g in grp.getgrall() if g.gr_name in groups]

#     for root, dirs, files in os.walk("/"):
#         for file in files:
#             try:
#                 path = os.path.join(root, file)
#                 st = os.stat(path)
#                 if st.st_gid in group_gids and (st.st_mode & stat.S_IXGRP):
#                     if is_accessible(path, "x"):
#                         group_exec_files.append(path)
#             except Exception:
#                 continue
#     return group_exec_files