# Generated by Django 5.1.7 on 2025-03-15 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0008_alter_weatherdata_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weatherdata',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='weatherdata',
            name='lon',
        ),
    ]
