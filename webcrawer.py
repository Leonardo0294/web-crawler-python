import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

def get_page_content(url):
    """
    Función para obtener el contenido HTML de una página web dada una URL.
    
    Args:
        url (str): La URL de la página a obtener.
        
    Returns:
        str or None: El contenido HTML de la página en formato de texto, o None si ocurre un error.
    """
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
    """
    Función para extraer encabezados (h1) y párrafos (p) de una página HTML dada su contenido.
    
    Args:
        html_content (str): Contenido HTML de la página.
        
    Returns:
        tuple: Una tupla que contiene dos listas de strings, una para encabezados y otra para párrafos.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    headings = [str(tag) for tag in soup.find_all('h1')]
    paragraphs = [str(tag) for tag in soup.find_all('p')]
    return headings, paragraphs

def crawl_website(start_url):
    """
    Función principal para realizar el crawling de un sitio web a partir de una URL inicial.
    
    Args:
        start_url (str): La URL inicial desde la cual comenzar el crawling.
    """
    visited_urls = set()  # Conjunto para almacenar URLs visitadas
    results = {}          # Diccionario para almacenar resultados de encabezados y párrafos

    def crawl(url):
        """
        Función interna para realizar el crawling recursivo de una URL dada.
        
        Args:
            url (str): La URL actual a ser procesada.
        """
        if url in visited_urls:
            return
        visited_urls.add(url)

        print(f"Crawling: {url}")
        html_content = get_page_content(url)
        if not html_content:
            return

        headings, paragraphs = extract_headings_and_paragraphs(html_content)
        results[url] = headings + paragraphs

        # Se extraen enlaces de la página actual
        soup = BeautifulSoup(html_content, 'html.parser')
        links = [link['href'] for link in soup.find_all('a', href=True)]

        base_url = url  #

        for link in links:
            if link.startswith('http'):
                continue  
            elif link.startswith('/'):
                # Construir URL absoluta si el enlace comienza con '/'
                absolute_link = urljoin(base_url, link)
            else:
                continue 

            # Recursivamente continuar el crawling con el nuevo enlace encontrado
            crawl(absolute_link)

    # Se inicia el crawling desde la URL inicial
    crawl(start_url)

    # Se guardan resultados en un archivo JSON
    with open('crawl_results.json', 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == '__main__':
    # URL de inicio para el crawling
    start_url = 'https://www.infotec.com.pe/3-laptops-y-notebooks'
    crawl_website(start_url)
