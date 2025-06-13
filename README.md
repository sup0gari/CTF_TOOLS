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

# url_brute.py
This script performs a brute-force scan of URLs within a specified numeric range on a given base URL and directory.
It sends HTTP HEAD requests to each generated URL with spoofed User-Agent headers to check their availability.

### Requirement
- Python 3.6+
- `requests` library

### Usage
```bash
python3 url_brute.py
```
You will be asked to input:
- BASE URL (e.g. http://example.com)
- PAGES DIRECTORY (e.g. pages)
- START NUMBER (e.g. 1)
- END NUMBER (e.g. 100)
The script will scan URLs constructed as:
`<BASE URL>/<PAGES DIRECTORY>/<number>`
from start number to end number using concurrent HTTP HEAD requests.

### Example
```bash
ENTER BASE URL (e.g. http://example.com): http://testsite.com
ENTER PAGES DIRECTORY (e.g. pages): docs
ENTER START NUMBER (e.g. 1): 1
ENTER END NUMBER (e.g. 10): 10
```
It will scan:
```bash
http://testsite.com/docs/1
http://testsite.com/docs/2
...
http://testsite.com/docs/10
```

### Notes
- Uses HTTP HEAD requests to check URL existence and content length without downloading files.
- Reports URLs found with non-zero content length and warns if content length is zero or unknown.
- Uses threading to speed up scanning; default thread count is 10 (configurable in the script).
- Handles basic errors and interruptions gracefully.
- Make sure the target server allows HEAD requests; otherwise, you may get false negatives.

# CPDecrypt
This script decrypts cpassword strings used in Microsoft Group Policy Preferences (GPP).
It uses a known AES key and initialization vector (IV) to perform AES-CBC decryption of the base64-encoded cpassword.
The decrypted output is then unpadded using PKCS#7 and decoded from UTF-16LE to reveal the plaintext password.

### Requirement
- Python 3.X
- pycryptodome

### Usage
```bash
python3 cpdecrypt.py
```
You will be asked to input `cpassword`

### Example
```bash
CPASSWORD:
> Ohae/KyxnLuvdCQXUtAl+epa8/oo0AWvB2OtcQwYkFw=
[+] DECRYPTED PASSWORD:
P@ssw0rd123
```

### Notes
- The input cpassword must be a Base64-encoded string.
- The script uses a fixed AES-128-CBC key and IV specific to Windows GPP cpassword encryption.
- The decrypted output is PKCS#7 padded and encoded in UTF-16LE; incorrect padding or invalid input will cause errors.