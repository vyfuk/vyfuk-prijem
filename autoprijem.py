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
    

def _join_all_pdfs(directory, outfile_name, DUPLEX=True):
    print('Making %s' % outfile_name)
    def get_number_of_pages(filename):  
            pdfinfo = subprocess.Popen(['pdfinfo','-meta', filename], stdout=subprocess.PIPE)
            out, err = subprocess.Popen(['grep', 'Pages:'], stdin=pdfinfo.stdout, stdout=subprocess.PIPE).communicate()
            print(filename, out, err)
            return int(out.split()[-1])

    total_numpages = 0
    files = os.listdir(directory)
    files.sort()
    to_join = []
    temp_infix = datetime.date.today().isoformat()

    
    for fname in files:
        if fname[-4:] not in ['.pdf', '.PDF'] :
            continue
        fname.replace(' ', '\\ ')
        numpages = get_number_of_pages(os.path.join(directory, fname))
        total_numpages += numpages        
        if numpages % 2 and DUPLEX:
            temp_file_path = os.path.join(TEMP_DIR, '%s%s_joined.pdf' % (fname[:-4], temp_infix))
            command = 'pdfjoin %s white.pdf --outfile "%s" -q ' % (
                os.path.join(directory, fname), 
                temp_file_path)
            os.system(command)
            #~ os.system ( 'pdfjoin "'+os.path.join(priklad, fname)+'" white.pdf --outfile "'+os.path.join('out/joined/',fname[:-4] + '_joined.pdf')  + '" -q' )
            to_join.append(temp_file_path)
            total_numpages += 1
        else:
            to_join.append(os.path.join(directory, fname))
    #~ print(to_join)    

    command = 'pdfjoin --rotateoversize \'false\'  %s --outfile %s' % (
        ' '.join(map(lambda x:'"'+x+'"', to_join)),
        os.path.join(outfile_name))
    os.system(command)
    #~ os.system('pdfjoin --rotateoversize \'false\' ' +' '.join(map(lambda x:'"'+x+'"', to_join)) + ' --outfile na_tlac/'+priklad+'_joined_duplex.pdf')
    produced_numpages = get_number_of_pages(outfile_name)

    if total_numpages != produced_numpages:
        print('Number of produced pages for outfile %s : %d' % (outfile_name, produced_numpages))
        print('Number of expected pages : %d' % total_numpages)
        print('These numbers differ, something has gone wrong!')

#~ _join_all_pdfs('./download/rocnik28/serie1/uloha-1', 'download/rocnik28/serie1/uloha1_joined_duplex.pdf')
#~ 
#~ exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-D', '--download', action='store_true') 
    parser.add_argument('-J', '--join', action='store_true')
    
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

    if args.join:
        if args.problems is None:
            problems = ['1', '2', '3', '4', '5', 'P', 'E', 'S']
        else:
            problems = args.problems
            if any(problem not in '12345PES' for problem in problems):
                raise Exception('Can\'t parse problems ' + str(problems))
        
        for problem in problems:
            problem_dir = os.path.join(DOWNLOAD_DIR,
                                            'rocnik%d' % args.rocnik, 
                                            'serie%d' % args.serie,
                                            'uloha-%s' % problem)
            output = os.path.join(DOWNLOAD_DIR,
                                            'rocnik%d' % args.rocnik, 
                                            'serie%d' % args.serie,
                                            'uloha%s_joined.pdf' % problem)
            _join_all_pdfs(problem_dir, output)
        

 
