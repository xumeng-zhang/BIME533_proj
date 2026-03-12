"""
Alternative download script for NHANES 2009-2010 data
Try accessing through the data page API
"""
import requests
from bs4 import BeautifulSoup
import re

def find_download_links():
    """Find the correct download links by accessing the NHANES data page"""

    # Try accessing the demographic data page
    demo_url = "https://wwwn.cdc.gov/Nchs/Nhanes/2009-2010/DEMO_F.htm"
    oral_url = "https://wwwn.cdc.gov/Nchs/Nhanes/2009-2010/OHXDEN_F.htm"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    for name, doc_url in [('Demographics', demo_url), ('Oral Health', oral_url)]:
        print(f"\nChecking {name} documentation page: {doc_url}")
        try:
            response = requests.get(doc_url, headers=headers, timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Look for links to .XPT files
                xpt_links = soup.find_all('a', href=re.compile(r'\.XPT$', re.I))
                for link in xpt_links:
                    href = link.get('href')
                    print(f"  Found XPT link: {href}")

                # Also look for any mention of data file location
                text = soup.get_text()
                if '.XPT' in text or '.xpt' in text:
                    print(f"  Page mentions XPT files")

        except Exception as e:
            print(f"  Error: {e}")

    # Try the comprehensive data search page
    print("\n\nTrying comprehensive data search page...")
    search_url = "https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Demographics&CycleBeginYear=2009"
    print(f"URL: {search_url}")

    try:
        response = requests.get(search_url, headers=headers, timeout=30)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for download links
            all_links = soup.find_all('a', href=True)
            xpt_links = [link for link in all_links if '.XPT' in link.get('href', '').upper()]
            print(f"Found {len(xpt_links)} XPT links")
            for link in xpt_links[:5]:
                print(f"  {link.get('href')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    print("Searching for NHANES 2009-2010 download links...\n")
    find_download_links()
