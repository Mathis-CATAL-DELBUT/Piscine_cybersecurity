import requests
from bs4 import BeautifulSoup
import os

url = 'https://fr.wikipedia.org/wiki/M%C3%A9thode_des_moindres_carr%C3%A9s'
extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

response = requests.get(url)

all_html = BeautifulSoup(response.text, 'html.parser')

all_img = all_html.find_all("img")

srcs_img = []

for img in all_img:
    src = img.get("src")
    if (any(src.endswith(ext) for ext in extensions)):
        if (src.startswith("//")):
            src = "https:" + src
        else:
            src = "https://" + url.split("/")[2] + src
        srcs_img.append(src)
        print(src)


folder_path = "../photo"


for src in srcs_img:
    filename = src.split("/")[-1]
    response = requests.get(src)
    file_path = os.path.join(folder_path, filename)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Image '{filename}' téléchargée avec succès.")
    else:
        print(f"Échec du téléchargement de l'image '{filename}'. Code d'état : {response.status_code}")

