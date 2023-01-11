# Generated by Django 4.1.3 on 2023-01-04 12:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("genomeBact", "0003_alter_genome_size_alter_genome_start"),
    ]

    operations = [
        migrations.RenameField(
            model_name="transcript",
            old_name="transcript",
            new_name="ID",
        ),
        migrations.AddField(
            model_name="transcript",
            name="seq_cds",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="transcript",
            name="seq_nt",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="genome",
            name="chromosome",
            field=models.CharField(
                help_text="Chromosome name",
                max_length=30,
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="genome",
            name="size",
            field=models.IntegerField(
                help_text="Size of chromosome",
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(100000000),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="genome",
            name="start",
            field=models.IntegerField(
                default=1, validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
    ]