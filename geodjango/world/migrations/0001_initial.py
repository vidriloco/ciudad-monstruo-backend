# Generated by Django 4.2.7 on 2023-11-26 18:12

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('world', '0000_postgis'),
    ]

    operations = [
        migrations.CreateModel(
            name='VictimReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('date', models.DateField(blank=True, default=None, null=True)),
                ('time', models.CharField()),
                ('felony', models.CharField()),
                ('category', models.CharField()),
                ('reporter_genre', models.CharField()),
                ('reporter_age', models.IntegerField()),
                ('reporter_type', models.CharField()),
                ('reporter_status', models.CharField()),
                ('competence', models.CharField()),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
    ]
