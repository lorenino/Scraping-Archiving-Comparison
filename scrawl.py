import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, init
from tqdm import tqdm
import pandas as pd
import datetime  

# Initialize Colorama for color handling in the terminal
init(autoreset=True)

def fetch(url):
    """Fetch the content of the URL and return the response object."""
    try:
        response = requests.get(url, timeout=10)
        return response
    except requests.RequestException:
        return None

def process_page(url, base_domain):
    """Process a single page: fetch content and find all valid links."""
    response = fetch(url)
    if not response or not response.ok:
        return set(), url

    soup = BeautifulSoup(response.text, 'html.parser')
    found_links = set()
    for link in soup.find_all('a', href=True):
        full_url = urljoin(url, link['href'])
        parsed_url = urlparse(full_url)
        # Filter out unwanted URLs
        if not parsed_url.netloc.endswith(base_domain) or parsed_url.query or parsed_url.fragment:
            continue
        if parsed_url.path.lower().endswith(('.jpg', '.jpeg', '.pdf', '.png', '.gif', '.mp4', '.mp3', '.avi', '.mov', '.wmv')):
            continue
        found_links.add(full_url)
    return found_links, url

def crawl_site(start_url, base_domain, max_workers=10):
    """Crawl the website starting from start_url, using multithreading."""
    visited = set()
    to_visit = set([start_url])

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        with tqdm(total=0) as pbar:
            while to_visit:
                futures = {executor.submit(process_page, url, base_domain): url for url in to_visit if url not in visited}
                to_visit.clear()
                for future in as_completed(futures):
                    urls, url = future.result()
                    visited.add(url)
                    to_visit.update(u for u in urls if u not in visited and u not in to_visit)
                    pbar.update(1)
                    pbar.total = len(to_visit)
    return visited

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web crawler")
    parser.add_argument("start_url", help="URL to start crawling from")
    args = parser.parse_args()

    base_domain = urlparse(args.start_url).netloc
    start_url = args.start_url

    visited_pages = crawl_site(start_url, base_domain)
    sorted_pages = sorted(visited_pages)  # Sort visited pages alphabetically

    # Generate the file name with date, time, and base name
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"visited_urls_{base_domain}_{timestamp}.xlsx"

    # Create a DataFrame and save to an Excel file
    df = pd.DataFrame(sorted_pages, columns=['URL'])
    df.to_excel(filename, index=False)

    print(f"{Fore.MAGENTA}Crawling complete. Total pages visited: {len(sorted_pages)}")
    print(f"URLs saved to {filename}")
