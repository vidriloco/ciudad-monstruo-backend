# Generated by Django 4.2.7 on 2024-01-15 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0008_alter_agebvictimreport_ageb'),
    ]

    operations = [
        migrations.AddField(
            model_name='victimreport',
            name='source',
            field=models.CharField(default='Fiscalia'),
            preserve_default=False,
        ),
    ]