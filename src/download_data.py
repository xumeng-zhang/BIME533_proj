"""Download NHANES 2009-2010 data files"""
import requests
import os

def download_nhanes_file(url, output_path):
    """Download a file from NHANES website"""
    print(f"Downloading from {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    response = requests.get(url, headers=headers, allow_redirects=True, timeout=60)

    if response.status_code == 200:
        # Check if we got HTML (error page) or actual data
        content_type = response.headers.get('content-type', '')
        if 'text/html' in content_type:
            print(f"ERROR: Got HTML page instead of data file")
            print(f"Status code: {response.status_code}")
            print(f"URL: {response.url}")
            print(f"First 200 chars: {response.text[:200]}")
            return False

        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded to {output_path} ({len(response.content)} bytes)")
        return True
    else:
        print(f"ERROR: Status code {response.status_code}")
        return False

# Create data directory if needed
os.makedirs('data/', exist_ok=True)

# Try different URL patterns for NHANES 2009-2010
base_patterns = [
    "https://wwwn.cdc.gov/Nchs/Nhanes/2009-2010/{filename}",
    "https://wwwn.cdc.gov/nchs/nhanes/2009-2010/{filename}",
]

files_to_download = {
    'DEMO_F.XPT': 'data/DEMO_F.XPT',
    'OHXDEN_F.XPT': 'data/OHXDEN_F.XPT'
}

for filename, output_path in files_to_download.items():
    downloaded = False
    for pattern in base_patterns:
        url = pattern.format(filename=filename)
        print(f"\nTrying: {url}")
        if download_nhanes_file(url, output_path):
            downloaded = True
            break

    if not downloaded:
        print(f"\nFailed to download {filename} from all URL patterns")
        print("\nPlease manually download the files from:")
        print("https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?BeginYear=2009")

print("\nChecking downloaded files:")
for output_path in files_to_download.values():
    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print(f"{output_path}: {size:,} bytes")
    else:
        print(f"{output_path}: NOT FOUND")
