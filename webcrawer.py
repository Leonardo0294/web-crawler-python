import requests
from bs4 import BeautifulSoup
import json

def get_page_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la página {url}: {e}")
        return None

def extract_headings_and_paragraphs(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    headings = [str(tag) for tag in soup.find_all('h1')]
    paragraphs = [str(tag) for tag in soup.find_all('p')]
    return headings, paragraphs

def crawl_website(start_url):
    visited_urls = set()
    results = {}

    def crawl(url):
        if url in visited_urls:
            return
        visited_urls.add(url)

        print(f"Crawling: {url}")
        html_content = get_page_content(url)
        if not html_content:
            return

        headings, paragraphs = extract_headings_and_paragraphs(html_content)
        results[url] = headings + paragraphs

        # Extract links from the current page
        soup = BeautifulSoup(html_content, 'html.parser')
        links = [link['href'] for link in soup.find_all('a', href=True)]

        for link in links:
            if link.startswith('http'):  # Filter external links
                continue
            elif link.startswith('/'):  # Handle relative links
                absolute_link = start_url.rstrip('/') + link
            else:
                continue

            crawl(absolute_link)

    crawl(start_url)

    # Save results to JSON file
    with open('crawl_results.json', 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == '__main__':
    start_url = 'https://example.com'  # Replace with the starting URL
    crawl_website(start_url)
