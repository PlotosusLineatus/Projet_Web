# Generated by Django 4.1.3 on 2023-01-04 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("genomeBact", "0006_transcript_start_transcript_stop"),
    ]

    operations = [
        migrations.AddField(
            model_name="transcript",
            name="description",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AddField(
            model_name="transcript",
            name="gene",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="transcript",
            name="gene_biotype",
            field=models.CharField(default="protein coding", max_length=100),
        ),
    ]