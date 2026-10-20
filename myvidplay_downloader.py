import cloudscraper
import requests
import random
import string
import time
import re
import sys
import os
from urllib.parse import urlparse

def get_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def download_video(url_input):
    # Use cloudscraper to bypass Cloudflare/Bot protection
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    embed_url = None
    
    # Extract filename slug from the input URL
    slug = url_input.strip('/').split('/')[-1]
    
    # Ensure VIDEO directory exists
    if not os.path.exists("VIDEO"):
        os.makedirs("VIDEO")
    
    output_filename = os.path.join("VIDEO", slug + ".mp4")

    print(f"[*] Processing: {url_input}")

    # 1. Resolve CandidShiny to find the Embed URL
    if "candidshiny.com" in url_input:
        print(f"[*] Bypassing protection on CandidShiny...")
        try:
            r = scraper.get(url_input)
            if r.status_code != 200:
                print(f"[-] Failed to access page. Status: {r.status_code}")
                return

            # Check if we were redirected DIRECTLY to the embed
            if "myvidplay.com" in r.url or "doodstream.com" in r.url or "dood." in r.url:
                print(f"[*] Detected redirect to Embed: {r.url}")
                embed_url = r.url
            else:
                # Look for iframe src
                match = re.search(r'iframe src="([^"]+)"', r.text)
                if match:
                    embed_url = match.group(1)
                    if embed_url.startswith('//'): 
                        embed_url = "https:" + embed_url
                else:
                    match = re.search(r'(https?://(?:myvidplay\.com|doodstream\.com|dood\.\w+|ds2play\.com)/e/[a-zA-Z0-9]+)', r.text)
                    if match:
                        embed_url = match.group(1)
        except Exception as e:
            print(f"[-] Error accessing CandidShiny: {e}")
            return
    else:
        embed_url = url_input
        match = re.search(r'/e/([a-z0-9]+)', embed_url)
        if match and slug == "e":
            output_filename = os.path.join("VIDEO", f"dood_{match.group(1)}.mp4")

    if not embed_url:
        print("[-] Could not find embed URL.")
        return

    print(f"[*] Target Embed: {embed_url}")

    # 2. Extract Video Details
    try:
        scraper.headers.update({"Referer": url_input})
        r = scraper.get(embed_url)
        html = r.text
        
        md5_match = re.search(r"'/pass_md5/([^']+)'", html)
        if not md5_match:
             md5_match = re.search(r"'/pass_md5/([^/]+)'", html)
        
        if not md5_match:
            print("[-] Could not find 'pass_md5' token.")
            return

        pass_md5_path = md5_match.group(1)
        token = pass_md5_path.split('/')[-1]
        
        parsed_uri = urlparse(embed_url)
        domain = f"{parsed_uri.scheme}://{parsed_uri.netloc}"
        pass_md5_url = f"{domain}/pass_md5/{pass_md5_path}"
        
        print(f"[*] Fetching video base: {pass_md5_url}")
        scraper.headers.update({"Referer": embed_url})
        time.sleep(1)
        
        r = scraper.get(pass_md5_url)
        base_video_url = r.text.strip()
        
        if not base_video_url.startswith("http"):
            print(f"[-] Invalid base video URL response.")
            return

        # 3. Final URL
        expiry = int(time.time() * 1000)
        random_suffix = get_random_string(10)
        final_url = f"{base_video_url}{random_suffix}?token={token}&expiry={expiry}"
        
        print(f"[*] Downloading to: {output_filename}")
        
        # 4. Download
        scraper.headers.update({
            "Range": "bytes=0-", 
            "Referer": domain + "/",
            "Connection": "keep-alive"
        })

        with scraper.get(final_url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(output_filename, 'wb') as f:
                downloaded = 0
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        mb = downloaded / (1024 * 1024)
                        sys.stdout.write(f"\r    Downloaded {mb:.2f} MB")
                        sys.stdout.flush()
        
        print(f"\n[+] Success: {output_filename}")

    except Exception as e:
        print(f"\n[-] Error: {e}")

import argparse



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="CandidShiny Video Downloader")

    parser.add_argument("url", nargs="?", help="Single CandidShiny or Embed URL")

    parser.add_argument("-l", "--list", help="Text file containing a list of URLs")

    

    args = parser.parse_args()



    if args.list:

        if os.path.isfile(args.list):

            print(f"[*] Batch processing file: {args.list}")

            try:

                with open(args.list, 'r') as f:

                    urls = [line.strip() for line in f if line.strip()]

                

                print(f"[*] Found {len(urls)} URLs to process.")

                

                for i, url in enumerate(urls):

                    print(f"\n--- Processing {i+1}/{len(urls)} ---")

                    download_video(url)

                    if i < len(urls) - 1:

                        wait_time = random.uniform(2, 5)

                        print(f"[*] Waiting {wait_time:.1f} seconds...")

                        time.sleep(wait_time)

            except Exception as e:

                print(f"[-] Error reading file: {e}")

        else:

            print(f"[-] File not found: {args.list}")

    elif args.url:

        download_video(args.url)

    else:

        parser.print_help()


