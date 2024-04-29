import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", help="Generate OTP")
    parser.add_argument("-k", help="Key for OTP")

    args = parser.parse_args()
    if (args.g):
        print(args.g)
    if (args.k):
        print(args.k)

main()