# Generated by Django 4.1.4 on 2022-12-28 17:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genomeBact', '0002_alter_annotation_gene_biotype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genome',
            name='size',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100000000)]),
        ),
        migrations.AlterField(
            model_name='genome',
            name='start',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100000000)]))]),
        ),
    ]
