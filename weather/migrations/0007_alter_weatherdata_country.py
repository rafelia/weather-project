# Generated by Django 5.1.7 on 2025-03-15 20:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0006_alter_countrydata_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherdata',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.countrydata'),
        ),
    ]
