import requests
from bs4 import BeautifulSoup

# URL elegida
url = 'https://www.mercadolibre.com.ar/c/autos-motos-y-otros#menu=categories'

# Realizar la solicitud HTTP
response = requests.get(url)

# Obtener el texto plano y pasarlo a BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Búsqueda de las imágenes por clase
results = soup.find_all('img', class_="dynamic-carousel__img")

# Mostrar las URLs de las imágenes por consola
for img in results:
    print(img['data-src'])
