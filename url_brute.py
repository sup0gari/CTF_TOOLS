#!/usr/bin/env python3

import requests
import sys
from concurrent.futures import ThreadPoolExecutor

NUM = 90
TIMEOUT = 3
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

def check_url(url):
    try:
        response = requests.head(url, headers=HEADERS, timeout=TIMEOUT)
        if response.status_code == 200:
            content_length = response.headers.get("Content-Length")
            try:
                length = int(content_length)
            except (TypeError, ValueError):
                length = None

            if length == 0 or length is None:
                warn(f"Found but empty (0 bytes or unknown size): {url}")
            else:
                ok(f"Found: {url} (Content-Length: {length} bytes)")
            return url
        else:
            warn(f"Not found: {url} (status: {response.status_code})")
    except requests.RequestException as e:
        warn(f"Error: {url} ({e})")
    return None

def main():
    try:
        print("\n" + "=" * NUM)
        print(r"""
 ____ _____________.____      ____________________ ____ _________________________
|    |   \______   \    |     \______   \______   \    |   \__    ___/\_   _____/
|    |   /|       _/    |      |    |  _/|       _/    |   / |    |    |    __)_ 
|    |  / |    |   \    |___   |    |   \|    |   \    |  /  |    |    |        \
|______/  |____|_  /_______ \  |______  /|____|_  /______/   |____|   /_______  /
                 \/        \/         \/        \/                            \/ 
        """)
        print("=" * NUM + "\n")

        url_base = input("Enter base URL (e.g. http://example.com): ").rstrip("/") + "/"
        directory = input("Enter pages directory (e.g. pages): ").strip("/")
        url = f"{url_base}{directory}/"
        start = int(input("Enter start number (e.g. 1): "))
        end = int(input("Enter end number (e.g. 100): "))

        info(f"Scanning URLs from {url}{start} to {url}{end}\n")

        urls = [f"{url}{i}" for i in range(start, end + 1)]

        with ThreadPoolExecutor(max_workers=THREADS) as executor:
            results = list(executor.map(check_url, urls))

        found_urls = [u for u in results if u is not None]

        if found_urls:
            ok(f"Found {len(found_urls)} URLs:")
            for found_url in found_urls:
                info(found_url)
        else:
            warn("No URLs found.")
        return 0
    except KeyboardInterrupt:
        warn("Interrupted by user. Exiting...")
        return 1
    except Exception as e:
        warn(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())