#!/usr/bin/env python3

import os
import pwd
import grp
import stat
import subprocess
import socket
import fnmatch
import re
import getpass

NUM = 85
EXTENSIONS = ['bak', 'swp', 'kdbx', 'txt']
KEYWORDS = ['password', 'passwd', 'pass', 'pwd', 'sql', 'mysql', 'sqlite',
            'mongo', 'mongodb', 'mariadb', 'redis', 'db']
DIRS = ['/var', '/home', '/etc', '/backup', '/backups', '/usr']
EXCLUDE_DIRS = ['/proc', '/sys', '/dev', '/run', '/snap', '/mnt']
CRON_DIRS = ['/etc/cron.d/', '/etc/crontab']
CURRENT_USER = getpass.getuser()
CURRENT_GROUPS = [grp.getgrgid(g).gr_name for g in os.getgroups()]

def print_line():
    print("=" * NUM)

def print_banner():
    print_line()
    print("\033[91m" + r"""
.__  .__      __________        .__                            
|  | |__| ____\______   \_______|__|__  __ ____   ______ ____  
|  | |  |/    \|     ___/\_  __ \  \  \/ // __ \ /  ___// ___\ 
|  |_|  |   |  \    |     |  | \/  |\   /\  ___/ \___ \\  \___ 
|____/__|___|  /____|     |__|  |__| \_/  \___  >____  >\___  >
             \/                               \/     \/     \/ 
    """ + "\033[0m")
    print_line()

def info(msg):
    print("\033[94m[*] {}\033[0m".format(msg))

def warn(msg):
    print("\033[91m[-] {}\033[0m".format(msg))
    
def ok(msg):
    print("\033[92m[+] {}\033[0m".format(msg))

def is_accessible(path, mode):
    return os.access(path, mode)

def run_command(cmd, silent_error=False):
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL if silent_error else subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return None if silent_error else str(e)
    except Exception:
        return None

def get_current_user():
    info("Current User Info:")
    print("  - User: {}".format(CURRENT_USER))
    print("  - Groups: {}".format(", ".join(CURRENT_GROUPS)))

def get_suid():
    info("Searching for SUID files...")
    output = run_command(['find', '/', '-perm', '-4000', '-type', 'f'], silent_error=True)
    if not output:
        warn("Failed to search for SUID files")
        return
    files = output.splitlines()
    for path in files:
        try:
            st = os.lstat(path)
            file_owner = pwd.getpwuid(st.st_uid).pw_name
            if is_accessible(path, os.X_OK):
                ok("{} (owner: {})".format(path, file_owner))
        except:
            continue

def get_sudo():
    info("Running `sudo -l`...")
    output = run_command(['sudo', '-l', '-n'], silent_error=True)
    if output is None or "password for" in output.lower():
        answer = input("Do you know the password? (Y/n): ").strip().lower()
        if answer == 'n':
            warn("Skipping sudo -l because password is unknown")
            return
        try:
            subprocess.run(['sudo', '-l'], check=True)
        except subprocess.CalledProcessError:
            warn("Failed to run sudo -l with password")
    else:
        print(output)

def get_cron():
    info("Checking cron jobs...")
    user_cron = run_command(['crontab', '-l'], silent_error=True)
    if user_cron:
        print("User Crontab:\n" + user_cron)
    else:
        info("No User Crontab")

    for path in CRON_DIRS:
        if not os.path.isfile(path) or not is_accessible(path, os.R_OK):
            continue
        try:
            with open(path) as f:
                print("\n  - Contents of {}:".format(path))
                print(f.read())
            if is_accessible(path, os.W_OK):
                ok("You have write permission on {}".format(path))
        except Exception:
            pass

def get_processes():
    info("Running Processes (formatted):")
    output = run_command(['ps', 'aux'], silent_error=True)
    if not output:
        warn("Failed to get processes")
        return
    lines = output.split('\n')
    if lines:
        print("{:<10} {:<6} {:<6} {:<8} {:<6} {}".format("USER", "PID", "%CPU", "%MEM", "TTY", "COMMAND"))
        for line in lines[1:]:
            parts = line.split(None, 10)
            if len(parts) >= 11:
                print("{:<10} {:<6} {:<6} {:<8} {:<6} {}".format(parts[0], parts[1], parts[2], parts[3], parts[6], parts[10]))

def get_ports():
    info("Local Open Ports:")
    output = run_command(['ss', '-tulpn'], silent_error=True)
    if output:
        print(output)
    else:
        warn("Failed to get open ports")

def get_suspicious_files():
    info("Searching for suspicious files...")
    args = ['find', '/']
    for exclude in EXCLUDE_DIRS:
        args.extend(['-path', exclude, '-prune', '-o'])
    args.append('(')
    for i, ext in enumerate(EXTENSIONS):
        if i > 0:
            args.append('-o')
        args.extend(['-name', '*.' + ext])
    args.append(')')
    args.extend(['-type', 'f', '-print'])

    output = run_command(args, silent_error=True)
    if output:
        for line in output.splitlines():
            ok("Found: {}".format(line))
    else:
        warn("No matching files found or find failed")

def search_keywords():
    info("Searching for credential/DB keywords...")
    grep_args = []
    for keyword in KEYWORDS:
        grep_args += ['-e', keyword]
    try:
        output = run_command(['find'] + DIRS + ['-type', 'f', '-exec', 'grep', '-I', '-l', '-i'] + grep_args + ['{}', '+'], silent_error=True)
        if output:
            files = output.splitlines()
            for file in files:
                ok("Found keyword in: {}".format(file))
        else:
            info("No keyword matches found.")
    except Exception:
        warn("Keyword search failed")

FUNCTIONS = [
    get_current_user,
    get_suid,
    get_sudo,
    get_cron,
    get_processes,
    get_ports,
    get_suspicious_files,
    search_keywords,
]

def main():
    print_banner()
    for function in FUNCTIONS:
        try:
            function()
        except Exception as e:
            warn("{}() failed: {}".format(function.__name__, e))
        print_line()
        input("\n[Enter] Next")

if __name__ == "__main__":
    main()
