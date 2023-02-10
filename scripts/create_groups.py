from django.contrib.auth.models import Group, User
from django.db.models.functions import Now
from genomeBact.models import Profile

GROUPS = ['Admin', 'Reader', 'Validator', 'Annotator']

def create_groups():
    for group in GROUPS:
        new_group, created = Group.objects.get_or_create(name=group)

def create_admin():

    username = "admin"
    email="admin@mail.fr"
    password ="AZERTY3456"
    group_name="Admin"
    first_name = "SaNoSi"
    last_name = "ABOHER"
    phone_number="0678123423"

    user =  User.objects.create_user(username=username, email=email, password=password )
    group = Group.objects.get(name = group_name)
    user.groups.add(group)

    Profile.objects.create(user = user, name=username, first_name = first_name, last_name=last_name, phone_number=phone_number,
                                    group = group_name, last_connexion = Now())
 

def create_users():

    username = "El_Teckel"
    email="teckel@mail.fr"
    password ="AZERTY3456"
    group_name="Validator"
    first_name = "Sophie"
    last_name = "Fonfec"
    phone_number="0678123423"


    user =  User.objects.create_user(username=username, email=email, password=password )
    group = Group.objects.get(name = group_name)
    user.groups.add(group)

    Profile.objects.create(user = user, name=username, first_name = first_name, last_name=last_name, phone_number=phone_number,
                                    group = group_name, last_connexion = Now())

    username = "Chiwowwow"
    email="Chihuahua_doux@mail.fr"
    password ="AZERTY3456"
    group_name="Annotator"
    first_name = "Yves"
    last_name = "Remord"

    user =  User.objects.create_user(username=username, email=email, password=password )
    group = Group.objects.get(name = group_name)
    user.groups.add(group)

    Profile.objects.create(user = user, name=username, first_name = first_name, last_name=last_name, phone_number=phone_number,
                                    group = group_name, last_connexion = Now())

    username = "Long_Snoot"
    email="groofgroof@mail.fr"
    password ="AZERTY3456"
    group_name="Annotator"
    first_name = "Anna"
    last_name = "Tomie"

    user =  User.objects.create_user(username=username, email=email, password=password )
    group = Group.objects.get(name = group_name)
    user.groups.add(group)

    Profile.objects.create(user = user, name=username, first_name = first_name, last_name=last_name, phone_number=phone_number,
                                    group = group_name, last_connexion = Now())
    
    username = "Dawg"
    email="ouafouaf@mail.fr"
    password ="AZERTY3456"
    group_name="Reader"
    first_name = "Jean"
    last_name = "Peuplu"

    user =  User.objects.create_user(username=username, email=email, password=password )
    group = Group.objects.get(name = group_name)
    user.groups.add(group)

    Profile.objects.create(user = user, name=username, first_name = first_name, last_name=last_name, phone_number=phone_number,
                                    group = group_name, last_connexion = Now())



def run():
    create_groups()
    create_admin()
    create_users()
    print("Created default group and users.")
