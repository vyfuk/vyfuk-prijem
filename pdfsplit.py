import os, json, shutil
from PyPDF2 import PdfFileWriter, PdfFileReader
from collections import OrderedDict

def init_upload_me(split_path, upload_me_path, problems):
    back_up_path = upload_me_path + "/upload_me"
    if not os.path.exists(back_up_path):
        print("Vytvarim ./upload_me")

        for problem in problems:
            shutil.copytree(split_path + f'/uloha-{problem}', back_up_path + f'/uloha-{problem}')
        
        print("upload_me vytvoren.\n")
    else:
        print("upload_me uz existuje.\n")


def split_it(joined_and_split_dir, stranytxt_dir, problems):
    stranysouhlasi = True
    kdenesouhlasi = []
    
    for problem in problems:

        split_path = joined_and_split_dir + f'/zaloha_split/uloha-{problem}'
        joined_path = joined_and_split_dir + f'/joined_uloha-{problem}.pdf' 
        stranytxtpath = stranytxt_dir + f"/stranyprorozdeleni_uloha-{problem}.txt"

        print(f'uloha: {problem}')

        if not os.path.exists(split_path):
            os.makedirs(split_path)

        #nacteme ulozeny pocet stran
        with open(stranytxtpath,"r") as f:
            dictnarozdeleni = OrderedDict(json.load(f))

        
        with open(joined_path, "rb") as joinedf:
            reader = PdfFileReader(joinedf)
            joinedpages = reader.getNumPages()
            print(f"Pocet stran joined u{problem}: {joinedpages}")
        
            pozice = 0

            for pdf in dictnarozdeleni.keys():
                pages = dictnarozdeleni[pdf]
                outpath = split_path + pdf[pdf.find("uloha-")+7:]
                #print(str(pages).ljust(8), str(pozice).ljust(5), pdf )

                writer = PdfFileWriter()
                for i in range(pages):
                    writer.addPage(reader.getPage(pozice))
                    pozice += 1 #posouvame pozici

                with open(outpath,"wb") as outf:
                    writer.write(outf)
            print(f"Celkovy pocet stran vytvorenych pdf u{problem}: {pozice}")
            print()

        if pozice !=  joinedpages:
            stranysouhlasi = False
            kdenesouhlasi.append(problem)

    if stranysouhlasi:
        print("Strany sedi")
    else:
        print("Strany nesedi v techto ulohach")
        print(kdenesouhlasi)

    init_upload_me(joined_and_split_dir + f'/zaloha_split', joined_and_split_dir, problems)

if __name__ == "__main__":
    
    problems = ["1","2","3","4","5","P","E","S"]


    rocnik = input('napis cislo rocniku: ')
    serie = input('napis cislo serie: ')

    joined_and_split_dir = f'./corrected/rocnik{rocnik}/serie{serie}'
    stranytxt_dir = f"./download/rocnik{rocnik}/serie{serie}"

    split_it(joined_and_split_dir, stranytxt_dir, problems)
    