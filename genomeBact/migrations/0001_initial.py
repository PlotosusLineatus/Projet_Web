# Generated by Django 4.1.4 on 2022-12-28 16:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genome',
            fields=[
                ('specie', models.CharField(max_length=50, unique=True)),
                ('chromosome', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('size', models.IntegerField(max_length=10)),
                ('start', models.IntegerField(default=1, max_length=10, validators=[django.core.validators.MaxValueValidator(models.IntegerField(max_length=10))])),
            ],
        ),
        migrations.CreateModel(
            name='transcript',
            fields=[
                ('transcript', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('chromosome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='genomeBact.genome')),
            ],
        ),
        migrations.CreateModel(
            name='annotation',
            fields=[
                ('gene', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('gene_biotype', models.IntegerField(max_length=10)),
                ('transcript_biotype', models.IntegerField(max_length=15)),
                ('gene_symbol', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=100)),
                ('transcript', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='genomeBact.transcript')),
            ],
        ),
    ]