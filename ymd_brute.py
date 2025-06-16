import requests
import os
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from functools import partial

NUM = 90
MAX_DAYS = 31
HEAD_TIMEOUT = 3
GET_TIMEOUT = 6
SAVE_DIR = "tmp_downloaded"
THREADS = 10

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
}

def info(msg):
    print(f"\033[94m[*] {msg}\033[0m")

def warn(msg):
    print(f"\033[91m[-] {msg}\033[0m")

def ok(msg):
    print(f"\033[92m[+] {msg}\033[0m")


def check_and_download(date_obj, url, extensions):
    year, month, day = date_obj
    try:
        datetime(year, month, day)
    except ValueError:
        return

    date_string = f"{year:04d}-{month:02d}-{day:02d}"
    filename = f"{date_string}.{extensions}"
    full_url = f"{url.rstrip('/')}/{filename}"

    try:
        head = requests.head(full_url, headers=HEADERS, timeout=HEAD_TIMEOUT)
        if head.status_code == 200:
            content_length = head.headers.get("Content-Length", "unknown")
            if content_length == "0":
                warn(f"Found but empty: {full_url} (0 bytes)")
            else:
                ok(f"Found: {full_url} (size: {content_length} bytes)")
                response = requests.get(full_url, headers=HEADERS, timeout=GET_TIMEOUT)
                if response.status_code == 200:
                    file_path = os.path.join(SAVE_DIR, filename)
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    info(f"Saved to {file_path}")
                else:
                    warn(f"Failed to download {full_url} (status: {response.status_code})")
        else:
            warn(f"Not found or forbidden: {full_url} ({head.status_code})")
    except Exception as e:
        warn(f"Error checking {full_url}: {e}")


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

        url = input("Base URL (e.g. http://example.com): ").strip()
        extensions = input("Extension (e.g. pdf, txt, zip): ").strip()
        year = int(input("Year (e.g. 2025): ").strip())
        month_from = int(input("Start month (1-12): ").strip())
        month_to = int(input("End month (1-12): ").strip())

        os.makedirs(SAVE_DIR, exist_ok=True)
        info(f"Checking days from 1 to {MAX_DAYS} in months {month_from} to {month_to}...\n")

        date_list = [
            (year, month, day)
            for month in range(month_from, month_to + 1)
            for day in range(1, MAX_DAYS + 1)
        ]

        info(f"Scan with {THREADS} threads...\n")

        func = partial(check_and_download, url=url, extensions=extensions)

        with ThreadPoolExecutor(max_workers=THREADS) as executor:
            executor.map(func, date_list)

        info("\nScan complete")
        return 0
    except KeyboardInterrupt:
        warn("\nInterrupted by user. Exiting...")
        return 1
    except Exception as e:
        warn(f"\nUnexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())