import argparse
import hashlib
import time
import hmac
from cryptography.fernet import Fernet

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

# key = b'NcjPjA88VYJFSp7Ev73WfovDVx9UkzQq7xz0VH7levQ='

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", help="Generate OTP")
    parser.add_argument("-k", help="Key for OTP")
    fernet = Fernet(b'NcjPjA88VYJFSp7Ev73WfovDVx9UkzQq7xz0VH7levQ=')

    args = parser.parse_args()
    if (args.g):
        with open("ft_otp.key", "w") as ft_otp:
            with open(args.g, "r") as file_param:
                key = file_param.read().split(" ")[0].split("\n")[0]
                if (len(key) < 64):
                    return print("File must be at least 64 characters long.")
                encode_key = fernet.encrypt(key.encode())
                ft_otp.write(encode_key.decode())
                print("Key was successfully saved in ft_otp.key.")

    if (args.k):
        with open("ft_otp.key", "r") as key_file:
            t = int(time.time() // 30)
            time_binary = t.to_bytes(8, byteorder='big')
            key = key_file.read().strip()
            key = fernet.decrypt(key.encode()).decode()
            k_bytes = bytes.fromhex(key)
            print(generate_totp(k_bytes, time_binary, 6))

main()
