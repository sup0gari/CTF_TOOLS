import requests
import os
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

NUM = 90
MAX_DAYS = 31
HEAD_TIMEOUT = 3
GET_TIMEOUT = 6
SAVE_DIR = "tmp_downloaded"
THREADS = 10

# SPOOFING THE HEADERS
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
}

def check_and_download(date_obj, url, extensions):
    year, month, day = date_obj
    try:
        datetime(year, month, day)
    except ValueError:
        return

    date_string = f"{year:04d}-{month:02d}-{day:02d}" # YOU CAN EDIT THIS
    filename = f"{date_string}.{extensions}"
    url = url.rstrip("/") + "/" + filename

    try:
        head = requests.head(url, headers=HEADERS, timeout=HEAD_TIMEOUT)
        if head.status_code == 200:
            content_length = head.headers.get("Content-Length", "unknown")
            if content_length == "0":
                print(f"[!] FOUND BUT EMPTY: {url} (0 bytes)")
            else:
                print(f"[+] FOUND: {url} (size: {content_length} bytes)")
                response = requests.get(url, headers=HEADERS, timeout=GET_TIMEOUT)
                if response.status_code == 200:
                    file_path = os.path.join(SAVE_DIR, filename)
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    print(f"    -> Saved to {file_path}")
                else:
                    print(f"[x] Failed to download {url} (status: {response.status_code})")
        else:
            print(f"[-] NOT FOUND OR FORBIDDEN: {url} ({head.status_code})")
    except Exception as e:
        print(f"[x] ERROR CHECKING {url}: {e}")

def main():
    try:
        print("\n" + "=" * NUM)
        print(r"""
_____.___.  _____  ________    ____________________ ____ _________________________
\__  |   | /     \ \______ \   \______   \______   \    |   \__    ___/\_   _____/
/   |   |/  \ /  \ |    |  \   |    |  _/|       _/    |   / |    |    |    __)_ 
\____   /    Y    \|    `   \  |    |   \|    |   \    |  /  |    |    |        \
/ ______\____|__  /_______  /  |______  /|____|_  /______/   |____|   /_______  /
\/              \/        \/          \/        \/                            \/ 
        """)
        print("=" * NUM + "\n")

        url = input("BASE URL (e.g. http://example.com): ").strip()
        extensions = input("EXTENSION (e.g. pdf, txt, zip): ").strip()
        year = int(input("YEAR (e.g. 2025): ").strip())
        month_from = int(input("START MONTH (1-12): ").strip())
        month_to = int(input("END MONTH (1-12): ").strip())

        os.makedirs(SAVE_DIR, exist_ok=True)
        print(f"[*] CHECKING DAYS FROM 1 TO {MAX_DAYS} IN MONTHS {month_from} TO {month_to}...\n")

        date_list = [
            (year, month, day)
            for month in range(month_from, month_to + 1)
            for day in range(1, MAX_DAYS + 1)
        ]

        print(f"\n[*] SCAN WITH {THREADS} THREADS...\n")

        with ThreadPoolExecutor(max_workers=THREADS) as executor:
            executor.map(lambda date: check_and_download(date, url, extensions), date_list)

        print("\n[*] SCAN COMPLETE")
        return 0
    except KeyboardInterrupt:
        print("\n[!] INTERRUPTED BY USER. EXITING...")
        return 1
    except Exception as e:
        print(f"\n[x] UNEXPECTED ERROR: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())