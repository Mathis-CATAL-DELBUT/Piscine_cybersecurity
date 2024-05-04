import argparse
import hashlib
import time
import hmac
from cryptography.fernet import Fernet
import pyotp
import qrcode
import base64
import tkinter as tk
from PIL import Image, ImageTk

def generate_totp(args, fernet, nb_char, label):
    '''
    - Generate a TOTP code with HOTP algorithm (HMAC-SHA1 + TOTP) rfc 4226
    https://datatracker.ietf.org/doc/html/rfc6238
    '''
    try :
        with open(args.k, "r") as key_file:
            t = int(time.time() // 30)
            time_binary = t.to_bytes(8, byteorder='big')
            key = key_file.read().strip()
            key = fernet.decrypt(key.encode()).decode()
            k_binary = bytes.fromhex(key)
    except:
        print("./ft_otp: error: key file not found.")


    hash = hmac.new(k_binary, time_binary, hashlib.sha1).digest()
    offset = hash[-1] & 0xf # 0xf = 00001111
    # 0x7f = 01111111
    # 0xff = 11111111
    binary = ((hash[offset] & 0x7f) << 24) | \
             ((hash[offset + 1] & 0xff) << 16) | \
             ((hash[offset + 2] & 0xff) << 8) | \
             (hash[offset + 3] & 0xff)

    result = str(binary % 10 ** nb_char)
    while len(result) < nb_char:
        result = "0" + result
    label.config(text=result)
    return result

def generate_qr_code(file_key, fernet, root):
    '''
    - Generate a QR code with the TOTP key
    - Print the QR code on the screen
    '''
    with open(file_key, "r") as key_file:
        key = key_file.read()
        key = fernet.decrypt(key.encode()).decode()

    binary_key = bytes.fromhex(key)
    key_32 = base64.b32encode(binary_key).decode()
    otp_url = pyotp.totp.TOTP(key_32).provisioning_uri("TOTP", issuer_name="Mcatal-d")

    # Generer le QR code
    qr = qrcode.QRCode()
    qr.add_data(otp_url)
    img = qr.make_image()
    img.save("qrcode.png")
    
    # Afficher le QR code
    image = Image.open("qrcode.png")
    image = image.resize((200, 200))
    image = ImageTk.PhotoImage(image)
    qr_label = tk.Label(root, image=image, width=200, height=200)
    qr_label.image = image
    qr_label.place(relx=0.5, rely=0.6, anchor="center")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", help="Generate OTP")
    parser.add_argument("-k", help="Key for OTP")
    fernet = Fernet(b'NcjPjA88VYJFSp7Ev73WfovDVx9UkzQq7xz0VH7levQ=')

    args = parser.parse_args()
    if (args.g):
        try:
            with open("ft_otp.key", "w") as ft_otp:
                with open(args.g, "r") as file_param:
                    key = file_param.read().split(" ")[0].split("\n")[0]
                    if (len(key) < 64):
                        return print("./ft_otp: error: key must be 64 hexadecimal characters.")
                    encode_key = fernet.encrypt(key.encode())
                    ft_otp.write(encode_key.decode())
                    print("Key was successfully saved in ft_otp.key.")
        except:
            print("./ft_otp: error: wrong file.")

    if (args.k):
        root = tk.Tk()
        root.title("TOTP")
        root.geometry("500x500")

        generate_button = tk.Button(root, text="Generate code", command=lambda: generate_totp(args, fernet, 6, code))
        generate_button.place(relx=0.5, rely=0.1, anchor="center")

        code = tk.Label(root, text="", bg="white", width=20, height=1)
        code.place(relx=0.5, rely=0.2, anchor="center")

        generate_button = tk.Button(root, text="Generate QR code", command=lambda: generate_qr_code(args.k, fernet, root))
        generate_button.place(relx=0.5, rely=0.3, anchor="center")

        root.mainloop()
        

main()
