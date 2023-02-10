# Projet OUAF 2023
ATIA Safiya - BOSSUT Noémie - HERMAN Simon

Cette application web d'annotation et d'analyse fonctionnelle de génomes bactériens a été conçue au sein de l'UE "Projet Programmation Web" du Master AMI2B. 

# Prérequis

Afin de pouvoir faire tourner le projet, vous avez besoin de [Django](https://www.djangoproject.com/) (**version**) et **?**


# Lancement de l'application
La liste des dépendances nécessaire au fonctionnement de l'application est disponible dans le fichier environment.yml.
Un environnement conda peut être utilisé : 

```bash
    git clone https://github.com/PlotosusLineatus/Projet_Web.git 
    cd Projet_Web
    conda env create --file environment.yml
    conda activate OUAF
```
Ce répertoire contient l'ensemble des dossiers et fichiers nécessaire, selon l'architecture suivante :
```bash
    Projet_Web/
├── db.sqlite3
├── environment.yml
├── genomeBact
│   ├── admin.py
│   ├── apps.py
│   ├── decorators.py
│   ├── forms.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── 0001_initial.cpython-310.pyc
│   │       └── __init__.cpython-310.pyc
│   ├── models.py
│   ├── __pycache__
│   │   ├── admin.cpython-310.pyc
│   │   ├── apps.cpython-310.pyc
│   │   ├── decorators.cpython-310.pyc
│   │   ├── forms.cpython-310.pyc
│   │   ├── __init__.cpython-310.pyc
│   │   └── models.cpython-310.pyc
│   ├── static
│   │   └── genomeBact
│   │       ├── admin.css
│   │       ├── img
│   │       │   ├── big_straf_left_seb.png
│   │       │   ├── big_straf_right_seb.png
│   │       │   ├── small_straf_left_seb.png
│   │       │   ├── small_straf_right_seb.png
│   │       │   ├── zoom_default_seb.png
│   │       │   ├── zoom_in_seb.png
│   │       │   ├── zoom_out_seb.png
│   │       │   ├── zoom_small_in_seb.png
│   │       │   └── zoom_small_out_seb.png
│   │       ├── link.js
│   │       ├── p1.png
│   │       ├── p2.png
│   │       ├── patternouaf.png
│   │       ├── styleshome.css
│   │       ├── styleslogin.css
│   │       ├── stylestab.css
│   │       ├── tab.js
│   │       ├── teckeltest.jpg
│   │       ├── transcript.js
│   │       └── user_detail.css
│   ├── templates
│   │   └── genomeBact
│   │       ├── admin.html
│   │       ├── base.html
│   │       ├── download_csv.html
│   │       ├── genome_create.html
│   │       ├── genome_detail.html
│   │       ├── home.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── results.html
│   │       ├── strand_error.html
│   │       ├── transcript_create.html
│   │       ├── transcript_detail.html
│   │       ├── transcript_list.html
│   │       ├── upload.html
│   │       ├── user_detail.html
│   │       └── workspace.html
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_forms.py
│   │   ├── test_models.py
│   │   ├── test_users.py
│   │   └── test_views.py
│   └── views
│       ├── home.py
│       ├── __pycache__
│       │   ├── home.cpython-310.pyc
│       │   ├── log.cpython-310.pyc
│       │   ├── results.cpython-310.pyc
│       │   ├── transcripts.cpython-310.pyc
│       │   └── users.cpython-310.pyc
│       ├── results.py
│       ├── transcripts.py
│       └── users.py
├── manage.py
├── ProjetWEB
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   ├── settings.cpython-310.pyc
│   │   ├── urls.cpython-310.pyc
│   │   └── wsgi.cpython-310.pyc
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── README.md
└── scripts
    ├── create_groups.py
    ├── dev.py
    ├── __init__.py
    ├── load_data.py
    ├── __pycache__
    │   ├── create_groups.cpython-310.pyc
    │   ├── __init__.cpython-310.pyc
    │   ├── load_data.cpython-310.pyc
    │   ├── reset_db.cpython-310.pyc
    │   └── utils.cpython-310.pyc
    ├── reset_db.py
    └── utils.py

```
En vous plaçant à la base du dossier, lancez les commandes suivantes
```bash
    python manage.py migrate
    python manage.py import my-data
    python manage.py runserver
```
Ouvrez votre navigateur et rendez vous à l'adresse indiquée. 

# Utilisation de OUAF
## Création d'un utilisateur

Vous ne pouvez pas accédez à l'application si vous n'êtes pas inscrit. Cliquez sur `register` et créez votre compte. Vous pouvez choisir le rôle qui vous sied le mieux entre:
- **Lecteur** : accès à la base de données sans possibilités d'interactions ou de modification du contenu.
- **Annotateur**: droits du lecteur + possibilité d'annoter des séquences
- **Validateur**: droit de l'annotateur + affecter et valider des annotations

Indiquez votre pseudo, mail, mdp et le rôle de votre choix. Vous pouvez désormais vous connecter!

## Page Home

La page Home vous dirige vers la majorité (ou l'ensemble à corriger) des fonctionnalités de l'application :

![image](https://user-images.githubusercontent.com/75751225/217904756-ea7b69e0-dc0d-4b90-854e-3277ecfe9a11.png)
Partez à la recherche d'un génome ou d'une séquence depuis le formulaire de recherche. Vous pouvez également cliquer sur `COLLECTION`si vous désirez avoir accès à l'ensemble de la base de données. 
L'onglet `PARAMETERS` vous permet d'acceder aux paramètres de votre compte, et de changer vos informations.
Si vous êtes connectés en tant qu'annotateur ou validateur, vous pouvez avoir accès l'onglet `WORKSPACE` qui vous relie aux travaux concernant les annotations.
