# Generated by Django 4.1.3 on 2023-02-04 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("genomeBact", "0003_transcript_length_nt_transcript_length_pep"),
    ]

    operations = [
        migrations.AddField(
            model_name="genome",
            name="length",
            field=models.IntegerField(null=True),
        ),
    ]
