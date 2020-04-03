import os, glob, shutil, json
problems = ['1', '2', '3', '4', '5', 'P', 'E', 'S']

manynames_path = "download/poradi_jmen_vicejmennych_resitelu.txt"

def back_up(path):
    back_up_path = path + "/back_up_switched"
    if not os.path.exists(back_up_path):
        print("Zalohuju")
        shutil.copytree(path, back_up_path)
        print("Switched download zalohovan.")
    else:
        print("Nezalohuju, zaloha uz existuje.")

def switch_name(path):
    for p in (glob.glob(path)):
        n = os.path.basename(p)
        path = os.path.dirname(p)
        cele_jmeno = n[:n.find('-')]
        za_krestnim = cele_jmeno[cele_jmeno.find('_')+1:]
        koncovka = n[n.find('-'):]

        if '_' in za_krestnim:
            if not cele_jmeno in manynames.keys():
                index_prijmeni = input(f'Kolikate slovo z {cele_jmeno} je prijmeni? Indexovano od 1. Kdyztak koukni do FKSDB.')
                manynames[cele_jmeno] = index_prijmeni
            names = cele_jmeno.split('_')
            bn = names.pop(int(manynames[cele_jmeno])-1)
            for name in names:
                bn += '_' + name  
            bn += koncovka

        else:
            bn =  za_krestnim + '_' + n[:n.find('_')] + koncovka

        #pocitac mi radi lidi jejichz jmeno zacina na "Ch" pod "C"
        if "ch" in bn[:2].lower():
            bn = "hzz" + bn[2:]

        os.rename(p,os.path.join(path, bn))
if __name__ == "__main__":
    rocnik = input('napis cislo rocniku: ')
    serie = input('napis cislo serie: ')
    path = f'download/rocnik{rocnik}/serie{serie}'

    #nacist manynames
    if os.path.exists(manynames_path):
        with open(manynames_path,"r") as f:
            manynames = json.load(f)
    else:
        manynames = {}

    #switch
    print("Prehazuju")
    for problem in problems:
        switch_name(path + f"/uloha-{problem}/*" )
    #save manynames
    with open(manynames_path,"w") as f:
        json.dump(manynames,f)


    #back up files
    back_up(path)