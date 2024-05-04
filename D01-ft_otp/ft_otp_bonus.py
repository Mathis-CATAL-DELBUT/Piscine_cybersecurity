import argparse
import hashlib
import time
import hmac
from cryptography.fernet import Fernet
import pyotp
import qrcode
import base64
import tkinter as tk

def generate_totp(key, time, nb_char):
    hash = hmac.new(key, time, hashlib.sha1).digest()
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
    # label.config(text=result)
    print(result)
    return result

def generate_qr_code(key):
    binary_key = bytes.fromhex(key)
    key_32 = base64.b32encode(binary_key).decode()
    otp_url = pyotp.totp.TOTP(key_32).provisioning_uri("TOTP", issuer_name="Mcatal-d")

    # Generer le QR code
    qr = qrcode.QRCode()
    qr.add_data(otp_url)
    img = qr.make_image()
    img.save("qrcode.png")
    

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
        try :
            with open(args.k, "r") as key_file:
                root = tk.Tk()
                t = int(time.time() // 30)
                time_binary = t.to_bytes(8, byteorder='big')
                key = key_file.read().strip()
                key = fernet.decrypt(key.encode()).decode()
                generate_qr_code(key)
                k_bytes = bytes.fromhex(key)
                totp = generate_totp(k_bytes, time_binary, 6)
                print(totp)
                generate_button = tk.Button(root, text="Generate", command=lambda: generate_totp(k_bytes, time_binary, 6))
                generate_button.place(x=100, y=100)
                root.mainloop()
        except:
            print("./ft_otp: error: key file not found.")

main()
