# MyVidPlay Downloader

An automated tool to download videos from `myvidplay.com`, `doodstream.com`, and `candidshiny.com`. 

## Features
- **All-in-One**: Supports both direct host links and CandidShiny redirects.
- **Anti-Bot Bypass**: Uses `cloudscraper` to simulate real browser behavior and bypass protections.
- **Batch Processing**: Download multiple videos from a text file.
- **Automatic Naming**: Files are named based on the URL slug for CandidShiny or the Host ID for direct links.
- **Portable**: Includes a standalone `.exe` for Windows.

## Usage

### Using the Executable (Windows)
```powershell
.\MyVidPlayDownloader.exe "URL"
# For batch mode
.\MyVidPlayDownloader.exe -l links.txt
```

### Using Python Source
```bash
python myvidplay_downloader.py "URL"
```

## Tools
- `myvidplay_downloader.py`: The main downloader engine.
- `scrape_links.py`: Crawler to gather unique links from CandidShiny categories.

## Requirements
- `cloudscraper`
- `requests`
- `beautifulsoup4`
- `Pillow` (for icon generation)
