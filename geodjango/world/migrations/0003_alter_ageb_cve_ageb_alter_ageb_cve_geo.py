# Generated by Django 4.2.7 on 2023-12-22 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0002_ageb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ageb',
            name='cve_ageb',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='ageb',
            name='cve_geo',
            field=models.BigIntegerField(),
        ),
    ]
