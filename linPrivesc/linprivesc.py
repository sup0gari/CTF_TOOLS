from common_imports import *
from utils import initial_banner, print_line, print_error
from others_info import check_basic, check_processes
from user_info import check_user, get_users
from su_info import check_sudoers
from cron_info import check_cron

def main():
    initial_banner()

    try:
        local_users = get_users()
    except Exception as e:
        print_error("get_users", e)
        local_users = []
    print_line()

    try:
        check_basic()
    except Exception as e:
        print_error("check_basic", e)
    print_line()

    try:
        check_user(local_users)
    except Exception as e:
        print_error("check_user", e)
    print_line()

    try:
        check_sudoers()
    except Exception as e:
        print_error("check_sudoers", e)
    print_line()

    try:
        check_processes(local_users)
    except Exception as e:
        print_error("check_processes", e)
    print_line()

    try:
        check_cron()
    except Exception as e:
        print_error("check_cron", e)
    print_line()

if __name__ == "__main__":
    main()