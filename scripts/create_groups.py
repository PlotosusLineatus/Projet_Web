from django.contrib.auth.models import Group, User
from genomeBact.models import Profile

GROUPS = ['Admin', 'Lecteur', 'Validateur', 'Annotateur']

def create_groups():
    for group in GROUPS:
        new_group, created = Group.objects.get_or_create(name=group)

def create_admin():

    username = "admin"
    email="admin@mail.fr"
    password1 ="AZERTY3456"
    password2="AZERTY3456"
    group="Admin"
    first_name = "SaNoSi"
    last_name = "ABOHER"

    user = User.objects.create(username=username, email=email, )
    group = Group.objects.get(name = group)
    user.groups.add(group)
            
    Profile.objects.create(user = user, name=user.username, group=group, first_name =first_name, last_name = last_name )
    print('us')

def create_users():

    username_1 = "El_Teckel"
    email_1="teckel@mail.fr"
    password1_1 ="AZERTY3456"
    password2_1="AZERTY3456"
    group_1="Validateur"
    first_name_1 = "Sophie"
    last_name_1 = "Fonfec"

    username_2 = "Chiwowwow"
    email_2="Chihuahua_doux@mail.fr"
    password1_2 ="AZERTY3456"
    password2_2="AZERTY3456"
    group_2="Annotateur"
    first_name_2 = "Yves"
    last_name_2 = "Remord"

    username_3 = "Long_Snoot"
    email_3="groofgroof@mail.fr"
    password1_3 ="AZERTY3456"
    password2_3="AZERTY3456"
    group_3="Annotateur"
    first_name_3 = "Anna"
    last_name_3 = "Tomie"

    user1 = User.objects.create(username=username_1, email=email_1, password = password1_1 )
    user2 = User.objects.create(username=username_2, email=email_2, password = password1_2 )
    user3 = User.objects.create(username=username_3, email=email_3, password = password1_3 )

    group = Group.objects.get(name = group)
    user.groups.add(group)
            
    Profile.objects.create(user = user1, name=user.username_1, group=group_1, first_name =first_name_1, last_name = last_name_1 )
    Profile.objects.create(user = user2, name=user.username_2, group=group_2, first_name =first_name_2, last_name = last_name_2 )
    Profile.objects.create(user = user3, name=user.username_3, group=group_3, first_name =first_name_3, last_name = last_name_3 )

print('us')


def run():
    create_groups()
    print("Created default group and permissions.")
