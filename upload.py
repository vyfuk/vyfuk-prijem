import os, os.path, glob

class ExistsError(Exception):
    pass

def check_and_save_submitids(local_path, submitids_path, problems):
    submitids = []
    errors = []

    for problem in problems:
        path_list = glob.glob( local_path[:-1] + f'uloha-{problem}/*')
        for pdf in path_list:
            idpozice = pdf.find("__")+2
            submitid = pdf[idpozice:idpozice+5]
            try:
                submitids.append(int(submitid))
            except:
                errors.append(pdf)

    if len(errors) > 0:
        for error in errors:
            print(error)
        raise ValueError(f"Nonvalid submitid(s) found")

    #else
    print("All submitids ok")

    #pokud uz neexistuje
    if os.path.exists(submitids_path):
        raise ExistsError(f"{submitids_path} already exists. Move to prevent overwrite.")

    with open(submitids_path, "w") as f:
        for submitid in submitids:
            print(f"{submitid},", file = f, end=" ")
        print(f"submitids saved at {submitids_path}")


def upload(local_path, remote_path, username, temp_path = "./temp"):
    """odkud kam kdo uploaduje"""
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    command = f"scp -r {local_path} {username}@fykos.cz:{remote_path}"
    os.system(command)


if __name__ == "__main__":

    problems = ['1', '2', '3', '4', '5', 'P', 'E', 'S']

    rocnik = int(input('napis cislo rocniku: '))
    serie = int(input('napis cislo serie: '))
    username = input('napis login na server: ')
    print()

    #bacha aby v te lokalni slozce nebylo jeste neco jineho
    local_path = f"./corrected/rocnik{rocnik}/serie{serie}/*"
    remote_path = f"/network/data/www/fykos/db.fykos.cz/upload/corrected/fykos/rocnik{rocnik}/serie{serie}"
    submitids_path = f"./corrected/rocnik{rocnik}/submitids.txt"

    submitids = check_and_save_submitids(local_path, submitids_path, problems)
    upload(local_path, remote_path, username)



