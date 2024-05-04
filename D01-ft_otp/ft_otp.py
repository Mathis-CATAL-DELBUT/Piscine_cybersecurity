import argparse
import hashlib
import time

import hmac
import binascii

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
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", help="Generate OTP")
    parser.add_argument("-k", help="Key for OTP")

    args = parser.parse_args()
    if (args.g):
        with open("ft_otp.key", "w") as key:
            with open(args.g, "r") as file:
                k = file.read().split(" ")[0].split("\n")[0]
                if (len(k) < 64):
                    return print("File must be at least 64 characters long.")
                key.write(k)
                print("Key was successfully saved in ft_otp.key.")

    if (args.k):
        with open("ft_otp.key", "r") as key_file:
            t = int(time.time() // 30)
            t_binary = t.to_bytes(8, byteorder='big')
            k = key_file.read().strip()  # Lecture de la clé depuis le fichier
            k_bytes = bytes.fromhex(k)
            print(generate_totp(k_bytes, t_binary, 6))

main()
