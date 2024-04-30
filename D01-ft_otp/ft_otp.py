import argparse
import hashlib

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", help="Generate OTP")
    parser.add_argument("-k", help="Key for OTP")

    args = parser.parse_args()
    if (args.g):
        with open("ft_otp.key", "w") as key:
            with open(args.g, "r") as file:
                str = file.read()
                if (len(str) < 64):
                    return print("File must be at least 64 characters long.")
                key.write(str)
                print("Key was successfully saved in ft_otp.key.")

    if (args.k):
        with open("ft_otp.key", "w") as key:
            hash = hashlib.sha256(args.k.encode())
            print(hash)

main()