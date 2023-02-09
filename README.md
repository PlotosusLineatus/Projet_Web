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
    ceci est une arborescence
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
