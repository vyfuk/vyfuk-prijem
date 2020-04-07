import os, os.path, datetime, subprocess

def upload(local_path, remote_path, username, temp_path = "./temp"):
    """odkud kam kdo stahuje"""
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    command = f"scp -r {local_path} {username}@fykos.cz:{remote_path}"
    os.system(command)
                

if __name__ == "__main__":
    
    #problems = ['1', '2', '3', '4', '5', 'P', 'E', 'S']

    rocnik = int(input('napis cislo rocniku: '))
    serie = int(input('napis cislo serie: '))
    username = input('napis login na server: ')

    local_path = f"/corrected/rocnik{rocnik}/serie{serie}/*"
    remote_path = f"/network/data/www/fykos/db.fykos.cz/upload/corrected/fykos/rocnik{rocnik}/serie{serie}"

    download(local_path, remote_path, username)



