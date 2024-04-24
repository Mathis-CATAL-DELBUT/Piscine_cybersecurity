import requests
import os
import argparse
import sys
import random
import string
from bs4 import BeautifulSoup
from colorama import Fore

def parse_args():

    recursive = False
    level = 5
    file_path = "../imgs/"
    site_path = None

    if len(sys.argv) < 2:
        print("Please provide a URL")
        exit(1)

    if ("-r" in sys.argv):
        recursive = True

    if ("-l" in sys.argv):
        level_index = sys.argv.index("-l")
        try:
            level = int(sys.argv[level_index + 1])
        except:
            print("Invalid level")
            exit(1)

    if ("-p" in sys.argv):
        file_path_index = sys.argv.index("-p")
        file_path = sys.argv[file_path_index + 1]
        if (not file_path.endswith("/")):
            file_path += "/"
    
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    site_path = sys.argv[-1]

    return site_path, recursive, level, file_path
    
def spider(file_path, url, recursive, level, visited_links = []):
    if (url not in visited_links and level >= 0):
        print("Downloading images from", Fore.BLUE, url, Fore.RESET)
    
    visited_links.append(url)

    extension = [".jpg", ".jpeg", ".png", ".gif", ".bnp"]

    try:
        content = requests.get(url)
    except:
        print("Invalid URL")
        return

    print("level = ", level)


    parser = BeautifulSoup(content.text, "html.parser")

    imgs = parser.find_all("img")

    srcs = []

    for img in imgs:
        src = img.get("src")
        if (src is None):
            continue
        if(src.startswith("//")):
            src = "https:" + src
        elif src.startswith("/"):
            src = "https://" + url.split("/")[2] + src
        elif src.startswith("http"):
            src = src
        elif src.startswith(".."):
            src = url + src[2:]
        else:
            src = "https://" + url.split("/")[2] + "/" + src
        if (any(src.endswith(ext) for ext in extension)):
            srcs.append(src)

    for src in srcs:
        image = requests.get(src)
        file_name = src.split("/")[-1]
        path = os.path.join(file_path + file_name)
        if (len(path) > 255):
            path = os.path.join(file_path + file_name[:255-len(file_name)])
        if (os.path.exists(path)):
            path = file_path + ''.join(random.choices(string.ascii_letters, k=5)) + file_name
        with open(path, "wb") as img_folder:
            img_folder.write(image.content)
            print("image", Fore.GREEN, src.split("/")[-1], Fore.RESET, "successfully downloaded")

    if recursive and level > 0:
        links = parser.find_all("a")
        for link in links:
            if link.get("href") and link.get("href").startswith("http") and link.get("href") not in visited_links:
                spider(file_path, link.get("href"), recursive, level - 1, visited_links)

def main():
    path, recursive, level, file_path = parse_args()
    visited_links = []
    spider(file_path, path, recursive, level, visited_links)

main()