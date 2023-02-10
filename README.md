# Projet OUAF 2023
ATIA Safiya - BOSSUT Noémie - HERMAN Simon

Cette application web d'annotation et d'analyse fonctionnelle de génomes bactériens a été conçue au sein de l'UE "Projet Programmation Web" du Master AMI2B. 

# Lancement de l'application :

La liste des dépendances nécessaire au fonctionnement de l'application est disponible dans le fichier environment.yml.
Un environnement conda peut être utilisé : 

```bash
    git clone https://github.com/PlotosusLineatus/Projet_Web.git 
    cd Projet_Web
    conda env create --file environment.yml
    conda activate OUAF
```

En vous plaçant à la base du dossier, lancez les commandes suivantes
```bash
    init_server.sh
```
Ouvrez votre navigateur et rendez vous à l'adresse http://127.0.0.1:8000/

Si init_server.sh ne parvient pas à créer les tables et y créer les données, se référer au document technique pour accéder aux commandes avancées.

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

# Détails du génome
En cliquant sur `COLLECTION` ou en faisant une recherche par génome, vous vous trouverez sur une page de résultat. De cette page vous avez l'option de télécharger les annotation compressées en zip ou d'en savoir plus sur un génome particulier. Dans ce cas, vous arriverez à la page suivante :

![image](https://user-images.githubusercontent.com/75751225/218156782-ae7ff0b7-cd0f-430d-bd3e-05f8aeb355fa.png)Cette page permets la visualisation du génome et des différents gènes présents dans la base de données. Pour naviguer, il suffit de cliquer sur les flèches directionnelles. Passer au dessus des gènes vous fera apparaitre l'identitifiant de celui-ci, et cliquer dessus vous amenera à sa page détaillée (*voir section suivante*). 
Cette liste de gène est également accessible sans visualisation, en scrollant jusqu'à l'identifiant désiré. Enfin, le bouton `UNIPROT` vous permettra d'acceder aux résultats de recherche de la banque de données Uniprot.

# Détails d'un gène
![image](https://user-images.githubusercontent.com/75751225/218156946-1105dc67-1286-4452-a181-06c0e75cad6e.png)
La page détaillée de chaque gène comprend : les séquence nucléotidique (et le bouton `BLASTn` associé), la séquence peptidique (et le bouton `BLASTp`associé). Le bouton `Uniprot` redirige vers le site éponyme, avec une recherche par numéro d'accession, essayez! Les différentes annotations si elles existent, sont visibles dans le cadre dédié. S'il ne s'agit pas d'annotations qui vous ont été confiées, il est impossible de les modifier. 
Vous pourrez aussi télécharger le fasta associé à ce gène.

Si vous êtes l'annotateur associé à ce gène, vous pourrez librement modifier les annotations. Attention, une fois que vous décidez des les envoyer pour validation, vous ne pourrez plus y toucher avant la réponse du validateur ! 
Si vous êtes validateur et que vous devez vérifier les annotations, il vous sera possible de les valider définitevement ou bien de les renvoyer pour plus de précisions à l'annotateur associé, en lui laissant un message.

# Espace de travail
![image](https://user-images.githubusercontent.com/55387021/218198938-32dabc23-d9ff-43c7-9b42-06f6cb10ddb8.png)
En tant que validateur, c'est ici que vous pourrez assigner des séquences à des annotateurs et valider, ou non, leurs annotations.
En tant qu'annotateur, l'espace `WORKSPACE` vous permet de connaitre les différents gènes qui vous ont été confiés, ainsi que les annotations en attente de validation.
Il est possible de télécharger un fasta avec tous les gènes à annoter.

# Paramètres Utilisateurs
Tout utilisateur peut changer ses informations, son mot de passe et même supprimer son compte. Attention c'est irreversible !
L'administrateur peut également changer les rôles de tous les utilisateurs.

# Page Admin
En tant qu'administrateur, vous pouvez assigner des gènes à annoter, les valider, les annoter. Vous pouvez également accéder à la page paramètres de tous utilisateurs ou encore ajouter/supprimer des génomes, des utilisateurs ou des gènes.

Enfin, la barre de navigation vous permet de retourner sur la page principale à tout moment, tout comme d'accéder à vos parametres utilisateur et modifier vos informations personneles et mot de passe.
