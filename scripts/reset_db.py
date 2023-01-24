

def run():


    import os
    import glob
    from django.core import management

    current_dir = os.getcwd()   


    db_path = current_dir + "/db.sqlite3"

    if os.path.isfile(db_path):
        print("Removing existing database ... ")
        os.remove(db_path)


    migrations_path = current_dir + "genomeBact/migrations/"

    files = glob.glob(migrations_path + "/*")


    if files:
        print("Removing existing migrations ... ")
        for file in files:
            os.remove(file)


    print("Creation des tables ...   \n\n\n")

    try:
        management.call_command("makemigrations", "genomeBact")
        management.call_command("migrate")

        print("Creation réussie")

    except Exception:

        print("Echec de création des tables")


    print("Chargement des données initiales ")
    try:

        management.call_command("runscript","load_data")
        print("Chargement réussi !")
    
    except Exception:

        print("Echec du chargement des données")



    