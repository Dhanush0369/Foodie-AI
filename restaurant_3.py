import requests
from bs4 import BeautifulSoup
import os

# URL of the menu page
url = "https://sardaarjirestaurant.com/menu.html"

def download_menu_images(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    menu_div = soup.find('div', class_='col-sm-offset-2 col-sm-8')
    if not menu_div:
        return "Menu container not found"

    img_tags = menu_div.find_all('img')
    os.makedirs('menus', exist_ok=True)

    downloaded_files = []
    for img in img_tags:
        img_url = img.get('src')
        if not img_url.startswith('http'):
            from urllib.parse import urljoin
            img_url = urljoin(url, img_url)
        filename = os.path.join('menus', os.path.basename(img_url))
        img_response = requests.get(img_url)
        img_response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(img_response.content)
        downloaded_files.append(filename)
    return downloaded_files

# Download images
files = download_menu_images(url)
print(files)



