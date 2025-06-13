import requests
import sys
from concurrent.futures import ThreadPoolExecutor

NUM = 90
TIMEOUT = 3
THREADS = 10

# SPOOFING THE HEADERS
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
}

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
                print(f"[!] FOUND BUT EMPTY (0 bytes or unknown size): {url}")
            else:
                print(f"[+] FOUND: {url} (Content-Length: {length} bytes)")
            return url
        else:
            print(f"[-] NOT FOUND: {url} (STATUS: {response.status_code})")
    except requests.RequestException as e:
        print(f"[!] ERROR: {url} ({e})")
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

        url_base = input("ENTER BASE URL (e.g. http://example.com): ").rstrip("/") + "/"
        directory = input("ENTER PAGES DIRECTORY (e.g. pages): ").strip("/")
        url = url_base + directory + "/"
        start = int(input("ENTER START NUMBER (e.g. 1): "))
        end = int(input("ENTER END NUMBER (e.g. 100): "))

        print(f"\n[*] SCANNING URLS FROM {url}{start} TO {url}{end}\n")
        urls = [f"{url}{i}" for i in range(start, end + 1)]

        with ThreadPoolExecutor(max_workers=THREADS) as executor:
            results = list(executor.map(check_url, urls))

        found_urls = [url for url in results if url is not None]

        if found_urls:
            print(f"\n[+] FOUND {len(found_urls)} URLS:")
            for url in found_urls:
                print(url)
        else:
            print("\n[-] NO URLS FOUND.")
        return 0
    except KeyboardInterrupt:
        print("\n[!] INTERRUPTED BY USER. EXITING...")
        return 1
    except Exception as e:
        print(f"\n[x] UNEXPECTED ERROR: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())