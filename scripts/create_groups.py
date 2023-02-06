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
    password2=""
    group=""

    user = User.objects.create(username=username, email=email, )
    group = Group.objects.get(name = group)
    user.groups.add(group)
            
    Profile.objects.create(user = user, name=user.username)
    print('us')

def run():
    create_groups()
    print("Created default group and permissions.")
