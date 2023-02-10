

def run():



    from django.core import management
    flag = False

    '''
    if os.path.isfile("./db.sqlite3"):
        print("Removing existing database ... ")
        os.remove("./db.sqlite3")


    migrations_path = "./genomeBact/migrations/"

    files = glob.glob(migrations_path + "/*")
    '''

    print("Creation des tables ...   \n\n\n")

    try:
        management.call_command("makemigrations", "genomeBact")
        management.call_command("migrate")

        print("Creation réussie")

    except Exception:

        print("Echec de création des tables")
        flag = True


    print("Chargement des données initiales ")
    try:

        management.call_command("runscript","load_data")
        print("Chargement réussi !")
    
    except Exception:

        print("Echec du chargement des données")
        flag = True

    if flag == False:

        return 0
    
    else:

        return 1