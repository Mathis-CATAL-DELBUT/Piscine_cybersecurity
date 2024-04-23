import requests
import os
from bs4 import BeautifulSoup
from colorama import Fore

url = "https://www.apple.com/"
extension = [".jpg", ".jpeg", ".png", ".gif", ".bnp"]

content = requests.get(url)

parser = BeautifulSoup(content.text, "html.parser")

imgs = parser.find_all("img")

srcs = []

for img in imgs:
    src = img.get("src")
    if(src.startswith("//")):
        src = "https:" + src
    elif src.startswith("/"):
        src = "https://" + url.split("/")[2] + src
    if (any(src.endswith(ext) for ext in extension)):
        srcs.append(src)

for src in srcs:
    image = requests.get(src)
    file_name = src.split("/")[-1]
    path = os.path.join("../photo/" + file_name)
    with open(path, "wb") as img_folder:
        img_folder.write(image.content)
        print("image", Fore.GREEN, src.split("/")[-1], Fore.RESET, "successfully downloaded")