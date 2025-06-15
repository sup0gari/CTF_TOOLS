# linPrivesc
linPrivesc is a simple Linux privilege escalation enumeration tool designed to gather important system information.

### Requirement
- Python 3.X

### Usage
```bash
python3 linprivesc.py
```

### Example
```bash
$ python3 linprivesc.py
[*] Current user: test-ubuntu
[*] Local users found in /etc/passwd:
    - test-ubuntu
[*] Hostname: supogari
[*] OS: Linux
[*] Kernel version: 5.15.167.4-microsoft-standard-WSL2
[*] Architecture: x86_64
...
```

### Notes
- The tool handles Ctrl+C gracefully to skip long-running scans.
- Avoids automated exploitation frameworks to encourage manual analysis.
- Some checks may require sudo privileges to access full information.
- Designed to be easily extendable and customizable.