import os, os.path, datetime, subprocess

def download(upload_path, download_path, username, temp_path = "./temp"):
    """odkud kam kdo stahuje"""
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    command = f"scp -r {username}@fykos.cz:{upload_path} {download_path}"
    os.system(command)
    
if __name__ == "__main__":
    
    rocnik = int(input('napis cislo rocniku: '))
    serie = int(input('napis cislo serie: '))
    username = input('napis login na server: ')

    download_path = f"./download/rocnik{rocnik}/serie{serie}"
    upload_path = f"/network/data/www/fykos/db.fykos.cz/upload/fykos/rocnik{rocnik}/serie{serie}/*"

    download(upload_path, download_path, username)
