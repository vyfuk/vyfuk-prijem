from PyPDF2 import PdfFileMerger, PdfFileReader
import glob
import os
import json
from collections import OrderedDict

def get_pages(file_name):
    with open(file_name,'rb') as file:
        pdf = PdfFileReader(file) 
        pg = pdf.getNumPages()
    return pg

def pdf_ok_writing(pdf):
    try:
        merger = PdfFileMerger()
        merger.append(pdf)
        merger.write("test_can_be_deleted.pdf")
        merger.close()
        return True
    except:
        return False

if __name__ == "__main__":

    problems = ["1","2","3","4","5","P","E","S"]
    white = 'white.pdf'

    rocnik = input('napis cislo rocniku: ')
    serie = input('napis cislo serie: ')

    exceptions = []

    for problem in problems:
        sumpg = 0
        sum_whites = 0
        print(f'uloha: {problem}')

        merger = PdfFileMerger()
        path_list = glob.glob(f'download/rocnik{rocnik}/serie{serie}/uloha-{problem}/*')
        pdf_list = [path for path in path_list if 'pdf' in path[-4:].lower()]
        dictnarozdeleni = OrderedDict()

        for pdf in pdf_list:
            if pdf_ok_writing(pdf):
                pages = 0 #at v tom nezustava bordel
                pages = get_pages(pdf)
                sumpg += pages
                merger.append(pdf)
                if pages % 2 != 0:
                    merger.append(white)
                    sum_whites += 1
                    pages += 1

                #tohle potrebuju jen ty, co se daji mergnout, tzn. i rozmergnout
                dictnarozdeleni.update( { pdf : pages } )

            #pokud to nespocita pages, tak to predpokladam ani nemergne...
            else:
                try: 
                    p = get_pages(pdf)
                    print("chyba writing: ", pdf)
                except:
                    print("chyba get_pages: ", pdf)

                exceptions.append(pdf)

        
        joined_path = f'download/rocnik{rocnik}/serie{serie}/joined_uloha-{problem}.pdf'
        merger.write(joined_path)
        merger.close()
        
        #az to nekdo bude chtit rozdelovat zpatky
        with open(f"download/rocnik{rocnik}/serie{serie}/stranyprorozdeleni_uloha-{problem}.txt","w") as f:
            json.dump(dictnarozdeleni,f)

        #tady uz jen vypisuju co se delo
        #print('Suma:   ', sumpg)
        #print('Whites: ',sum_whites)
        #print('S+W:    ',sumpg+sum_whites)

        jp = get_pages(joined_path)
        print('Joined pages: ', jp)
        print()

    print('Exceptions:')

    exc_path = f'download/rocnik{rocnik}/serie{serie}/exceptions'
    if not os.path.exists(exc_path):
        os.mkdir(exc_path)

    for exception in exceptions:
        print(exception)

        a = exception.find(f'uloha')
        #narve jim do jmena souboru slovo exceptions misto ulohy a tim je premisti do slozky exceptions
        os.rename(exception, exception[:a] + 'exceptions' + exception[a+7:])     