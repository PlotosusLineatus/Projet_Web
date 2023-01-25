# Generated by Django 4.1.5 on 2023-01-25 09:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Genome",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("specie", models.CharField(max_length=50, unique=True)),
                (
                    "chromosome",
                    models.CharField(
                        default="", help_text="Chromosome version name", max_length=30
                    ),
                ),
                (
                    "sequence",
                    models.TextField(
                        default="",
                        help_text="Copy FASTA sequence here",
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Sequence must be ATGCN", regex="^[ATCGN]+$"
                            )
                        ],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Transcript",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "transcript",
                    models.CharField(
                        help_text="Chromosome version name", max_length=50, unique=True
                    ),
                ),
                (
                    "seq_cds",
                    models.TextField(
                        default="",
                        validators=[
                            django.core.validators.RegexValidator(
                                regex="^[ARNDCQEGHILKMFPSTWYV]+$"
                            )
                        ],
                    ),
                ),
                (
                    "seq_nt",
                    models.TextField(
                        default="",
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Sequence must be ATGCN", regex="^[ATCGN]+$"
                            )
                        ],
                    ),
                ),
                ("start", models.IntegerField(null=True)),
                ("stop", models.IntegerField(null=True)),
                (
                    "chromosome",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transcript",
                        to="genomeBact.genome",
                    ),
                ),
            ],
        ),
    ]
