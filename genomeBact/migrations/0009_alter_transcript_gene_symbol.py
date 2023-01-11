# Generated by Django 4.1.3 on 2023-01-04 14:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("genomeBact", "0008_transcript_gene_symbol"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transcript",
            name="gene_symbol",
            field=models.CharField(
                max_length=20,
                null=True,
                validators=[django.core.validators.RegexValidator("^[A-Za-z0-9]+$")],
            ),
        ),
    ]
