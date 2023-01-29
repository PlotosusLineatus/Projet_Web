from django.contrib.auth.models import Group

GROUPS = ['Admin', 'Lecteur', 'Validateur', 'Annotateur']

def run():
    for group in GROUPS:
        new_group, created = Group.objects.get_or_create(name=group)

    print("Created default group and permissions.")