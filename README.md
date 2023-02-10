# Projet OUAF 2023
ATIA Safiya - BOSSUT Noémie - HERMAN Simon

Cette application web d'annotation et d'analyse fonctionnelle de génomes bactériens a été conçue au sein de l'UE "Projet Programmation Web" du Master AMI2B. 

# Prérequis

Afin de pouvoir faire tourner le projet, vous avez besoin de [Django](https://www.djangoproject.com/) (**version**) et **?**


# Lancement de l'application
Si les pré-requis sont satisfaits, placez vous dans le répertoire de travail désiré et récupérez le projet
```bash
    git clone https://github.com/PlotosusLineatus/Projet_Web
    cd Projet_Web
```
Ce répertoire contient l'ensemble des dossiers et fichiers nécessaire, selon l'architecture suivante :
```bash
    .
├── db.sqlite3
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
│   │       ├── 0001_initial.cpython-39.pyc
│   │       ├── 0002_remove_genome_id_alter_genome_chromosome_profile.cpython-39.pyc
│   │       ├── 0002_remove_genome_start_alter_genome_chromosome_and_more.cpython-39.pyc
│   │       ├── 0002_transcript_description_transcript_gene_and_more.cpython-39.pyc
│   │       ├── 0003_transcript_annotator_transcript_status.cpython-39.pyc
│   │       ├── 0003_transcript_length_nt_transcript_length_pep.cpython-39.pyc
│   │       ├── 0004_genome_length.cpython-39.pyc
│   │       └── __init__.cpython-39.pyc
│   ├── models.py
│   ├── __pycache__
│   │   ├── admin.cpython-39.pyc
│   │   ├── apps.cpython-39.pyc
│   │   ├── decorators.cpython-39.pyc
│   │   ├── forms.cpython-39.pyc
│   │   ├── __init__.cpython-39.pyc
│   │   ├── models.cpython-39.pyc
│   │   └── views.cpython-39.pyc
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
│   │       ├── logo_OUAF.png
│   │       ├── ouaf_b.png
│   │       ├── ouaf_g.png
│   │       ├── styleshome.css
│   │       ├── styleslogin.css
│   │       ├── stylestab.css
│   │       ├── tab.js
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
│   └── views.py
├── manage.py
├── ProjetWEB
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-39.pyc
│   │   ├── settings.cpython-39.pyc
│   │   ├── urls.cpython-39.pyc
│   │   └── wsgi.cpython-39.pyc
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
    │   ├── create_groups.cpython-39.pyc
    │   ├── __init__.cpython-39.pyc
    │   ├── load_data.cpython-39.pyc
    │   ├── reset_db.cpython-39.pyc
    │   └── utils.cpython-39.pyc
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
