import os, os.path, datetime, subprocess
import argparse

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
    parser = argparse.ArgumentParser()
    parser.add_argument('-D', '--download', action='store_true') 
    
    parser.add_argument('-r', '--rocnik', type=int, required=True)
    parser.add_argument('-s', '--serie', type=int, required=True)
    
    parser.add_argument('-p', '--problems', nargs='+')
    parser.add_argument('--login')
    
    args = parser.parse_args()
    
    if args.download:
        if args.login is None:
            raise Exception('Login name required. Specify by --login')
        #Todo : thrash the old files before downloading
        #       check for successful download 
        download(args.login, args.rocnik, args.serie)

