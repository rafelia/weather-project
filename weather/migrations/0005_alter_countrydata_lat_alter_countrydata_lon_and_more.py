# Generated by Django 5.1.7 on 2025-03-15 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0004_weatherdata_humidity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrydata',
            name='lat',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='countrydata',
            name='lon',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='lat',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='lon',
            field=models.CharField(max_length=15),
        ),
    ]
