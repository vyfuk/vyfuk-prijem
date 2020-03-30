import os
import json
from PyPDF2 import PdfFileWriter, PdfFileReader
from collections import OrderedDict


if __name__ == "__main__":
    
    problems = ["1","2","3","4","5","P","E","S"]

    rocnik = input('napis cislo rocniku: ')
    serie = input('napis cislo serie: ')

    stranysouhlasi = True
    kdenesouhlasi = []
    
    for problem in problems:
        print(f'uloha: {problem}')

        split_path = f'split/rocnik{rocnik}/serie{serie}/uloha-{problem}'
        if not os.path.exists(split_path):
            os.makedirs(split_path)

        joined_path = f'corrected/rocnik{rocnik}/serie{serie}/joined_uloha-{problem}.pdf'

        #nacteme ulozeny pocet stran
        with open(f"download/rocnik{rocnik}/serie{serie}/stranyprorozdeleni_uloha-{problem}.txt","r") as f:
            dictnarozdeleni = OrderedDict(json.load(f))

        
        with open(joined_path, "rb") as joinedf:
            reader = PdfFileReader(joinedf)
            joinedpages = reader.getNumPages()
            print(f"Pocet stran joined u{problem}: {joinedpages}")
        
            pozice = 0

            for pdf in dictnarozdeleni.keys():
                pages = dictnarozdeleni[pdf]
                outpath = "split" + pdf[8:]
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