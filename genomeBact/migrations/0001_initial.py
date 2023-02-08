# Generated by Django 4.1.4 on 2023-02-08 10:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genome',
            fields=[
                ('specie', models.CharField(max_length=50, unique=True)),
                ('chromosome', models.CharField(help_text='Chromosome version name', max_length=30, primary_key=True, serialize=False)),
                ('sequence', models.TextField(default='', help_text='Copy FASTA sequence here', validators=[django.core.validators.RegexValidator(message='Sequence must be ATGCN', regex='^[ATCGN]+$')])),
                ('length', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('group', models.CharField(choices=[('Admin', 'Admin'), ('Annotateur', 'Annotateur'), ('Validateur', 'Validateur')], default='Lecteur', max_length=40)),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transcript',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcript', models.CharField(help_text='Chromosome version name', max_length=50, unique=True)),
                ('seq_cds', models.TextField(default='', validators=[django.core.validators.RegexValidator(regex='^[ARNDCQEGHILKMFPSTWYV]+$')])),
                ('seq_nt', models.TextField(default='', validators=[django.core.validators.RegexValidator(message='Sequence must be ATGCN', regex='^[ATCGN]+$')])),
                ('length_nt', models.IntegerField(null=True)),
                ('length_pep', models.IntegerField(null=True)),
                ('start', models.IntegerField(null=True)),
                ('stop', models.IntegerField(null=True)),
                ('gene', models.CharField(default='', max_length=15)),
                ('gene_biotype', models.CharField(default='', max_length=10)),
                ('transcript_biotype', models.CharField(default='', max_length=15)),
                ('gene_symbol', models.CharField(default='', max_length=10)),
                ('description', models.CharField(default='', max_length=100)),
                ('status', models.CharField(choices=[('assigned', 'assigned'), ('annotated', 'annotated'), ('validated', 'validated'), ('empty', 'empty')], default='empty', max_length=200)),
                ('status_date', models.DateTimeField(null=True)),
                ('annotator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_annotate', to='genomeBact.profile')),
                ('chromosome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transcript', to='genomeBact.genome')),
                ('validator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='genomeBact.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Connexion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
