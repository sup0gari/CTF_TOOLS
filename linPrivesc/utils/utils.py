from common_imports import *
from constants import CURRENT_USER

def is_accessible(file_path, mode):
    try:
        st = os.stat(file_path)
        pw_entry = pwd.getpwnam(CURRENT_USER)
        uid = pw_entry.pw_uid
        gid = pw_entry.pw_gid
        gids = os.getgrouplist(CURRENT_USER, gid)

        mode_bit = {
            "r" : (stat.S_IRUSR, stat.S_IRGRP, stat.S_IROTH),
            "w" : (stat.S_IWUSR, stat.S_IWGRP, stat.S_IWOTH),
            "x": (stat.S_IXUSR, stat.S_IXGRP, stat.S_IXOTH)
        }.get(mode)

        if not mode_bit:
            raise ValueError(f"Unsupported mode '{mode}'")
        
        if st.st_uid == uid and (st.st_mode & mode_bit[0]):
            return True
        if st.st_gid in gids and (st.st_mode & mode_bit[1]):
            return True
        if st.st_mode & mode_bit[2]:
            return True
        
        return False
    except Exception:
        return False
    
def skip(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print(f"[!] Skipped {func.__name__}() via Ctrl+C.")
            return []
    return wrapper