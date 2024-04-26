from exif import Image
from colorama import Fore
import sys

extension = [".jpg", ".jpeg", ".png", ".gif", ".bnp"]

def scorpion():
    for img_path in sys.argv[1:]:
        if not any([img_path.endswith(ext) for ext in extension]):
            print(Fore.RED + "Invalid file format for image : ", Fore.RESET, img_path, Fore.RED, "Skipping...", Fore.RESET)
            continue
        print(Fore.GREEN + "==== IMAGE :", img_path, "==== ", Fore.RESET, "\n")
        with open(img_path, 'rb') as src:
            img = Image(src)
            print (Fore.LIGHTYELLOW_EX + "Exif_available : ", Fore.RESET, img.list_all(), Fore.CYAN, "\n\nExif data : ", Fore.RESET)
            for elt in img.list_all():
                print(elt, ":", img.get(elt))
        print("\n#################################################\n")





scorpion()