import cloudscraper
from bs4 import BeautifulSoup
import time
import random
import re
import sys

def scrape_candidshiny():
    base_url = "https://candidshiny.com/ilovethebeach"
    total_pages = 84
    unique_links = set()
    
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )

    print(f"[*] Starting scraper for {base_url}")
    print(f"[*] Total pages to scan: {total_pages}")
    print("[*] This process will take a few minutes.\n")

    try:
        for page in range(1, total_pages + 1):
            url = base_url if page == 1 else f"{base_url}/{page}"
            print(f"[*] Scanning page {page}/{total_pages}...", end=" ", flush=True)
            
            try:
                response = scraper.get(url, timeout=30)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    new_count = 0
                    for a_tag in soup.find_all('a', href=True):
                        href = a_tag['href']
                        if re.search(r'ilovethebeach-[a-zA-Z0-9]+$', href):
                            if not href.startswith('http'):
                                full_link = f"https://candidshiny.com{href}" if href.startswith('/') else f"https://candidshiny.com/{href}"
                            else:
                                full_link = href
                            
                            if full_link not in unique_links:
                                unique_links.add(full_link)
                                new_count += 1
                    print(f"Done (+{new_count}). Total: {len(unique_links)}")
                else:
                    print(f"Failed (Status: {response.status_code})")
            except Exception as e:
                print(f"Error: {e}")

            time.sleep(random.uniform(1.0, 2.5))

    except KeyboardInterrupt:
        print("\n[!] Interrupted. Saving links...")

    output_file = "links_to_download.txt"
    with open(output_file, "w") as f:
        for link in sorted(unique_links):
            f.write(link + "\n")

    print(f"\n[+] Success: {len(unique_links)} unique links saved to {output_file}")

if __name__ == "__main__":
    scrape_candidshiny()