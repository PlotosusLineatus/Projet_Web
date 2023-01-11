# Generated by Django 4.1.4 on 2022-12-28 17:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genomeBact', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='gene_biotype',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='transcript_biotype',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='genome',
            name='size',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(100000000)]),
        ),
        migrations.AlterField(
            model_name='genome',
            name='start',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(models.IntegerField(validators=[django.core.validators.MaxValueValidator(100000000)]))]),
        ),
    ]
