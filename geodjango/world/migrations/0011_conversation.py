# Generated by Django 4.2.10 on 2024-03-01 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0010_ageb_bike_accidents_events_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('message', models.TextField()),
                ('source', models.CharField()),
                ('userID', models.UUIDField()),
            ],
        ),
    ]