## hash_cracker.py
A simple hash identification and cracking tool using Python and John the Ripper.
Supports multiple hash formats with automatic detection via regex.
Useful for practicing basic cracking workflows and understanding how hash formats and cracking tools work internally.

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
