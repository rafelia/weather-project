# Generated by Django 5.1.7 on 2025-03-15 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0005_alter_countrydata_lat_alter_countrydata_lon_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrydata',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
