# hash_cracker.py
A simple hash identification and cracking tool using Python and John the Ripper.
Supports multiple hash formats with automatic detection via regex.
Useful for practicing basic cracking workflows and understanding how hash formats and cracking tools work internally.

### Requirement
- Python 3.X
- John the Ripper (You can use `john` command.)
- Wordlist (In this script, rockyou.txt is used as the wordlist for password cracking.)

### Usage
```bash
python3 hash_cracker.py
```
You can choose between two modes:
1. Analyze hash type only
2. Analyze hash type and attempt to crack it using John the Ripper

Once a hash is provided, the script uses regular expressions to identify possible hash formats.
If multiple formats are detected, it prompts you to choose one.
In cracking mode, it creates a temporary file and runs John the Ripper with the appropriate format.

### Example
```bash
$ python3 hash_cracker.py

Mode:
1: Analyze hash type
2: Analyze hash type and Crack it
> 2

Enter a hash:
> 5f4dcc3b5aa765d61d8327deb882cf99

[*] Cracking hash using format: raw-md5
...
[+] Password found: password
```

### Notes
If rockyou.txt is not found but rockyou.txt.gz exists, the script will prompt you to extract it:
```bash
Please extract rockyou.txt.gz at <PATH>
```
Supports various hash types including: MD5, NTLM, SHA-1, SHA-256, SHA-512, bcrypt, and NetNTLM.

# ymd_brute.py
A simple threaded script to download files from a server by brute-forcing file names in the format `YYYY-MM-DD.<EXT>`

### Requirement
- Python 3.7+
- `requests` library

### Usage
```bash
python3 ymd_brute.py
```
You will be asked to input:
- Base URL (e.g., http://example.com)
- File extension (e.g., pdf, txt, zip)
- Year (e.g., 2025)
- Starting and ending month (1 to 12)

### Example
```bash
BASE URL (e.g. http://example.com): http://example.com/reports
EXTENSION (e.g. pdf, txt, zip): pdf
YEAR (e.g. 2025): 2025
START MONTH (1-12): 1
END MONTH (1-12): 3
```
The script will try downloading 2025-01-01.pdf to 2025-03-31.pdf from the given URL.

### Notes
- The script spoofs the User-Agent header to bypass basic access control.
- Files are saved in the tmp_downloaded directory.
- Empty files (Content-Length: 0) are skipped but reported.
- Multi-threading is used.
- It ignores invalid calendar dates (e.g. February 30).