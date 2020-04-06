import os, os.path, datetime, subprocess

UPLOAD_DIR = "/network/data/www/fykos/db.fykos.cz/upload/fykos/"
DOWNLOAD_DIR = "./download/"
TEMP_DIR = "./temp"

def download(username, rocnik, serie):
    download_path = os.path.join(DOWNLOAD_DIR,
                                            'rocnik%d' % rocnik, 
                                            'serie%d' % serie)
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    command = "scp -r %s@fykos.cz:%s %s" % ( 
                                        username, 
                                        os.path.join(UPLOAD_DIR, 
                                            'rocnik%d' % rocnik, 
                                            'serie%d' % serie, 
                                            '*'),
                                        download_path
                                        )
    os.system(command)
    
if __name__ == "__main__":

    rocnik = int(input('napis cislo rocniku: '))
    serie = int(input('napis cislo serie: '))
    login = input('napis login na server: ')

    download(login, rocnik, serie)
