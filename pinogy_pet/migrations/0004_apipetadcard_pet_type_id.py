# Generated by Django 3.2.19 on 2024-02-21 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinogy_pet', '0003_apipetadcard'),
    ]

    operations = [
        migrations.AddField(
            model_name='apipetadcard',
            name='pet_type_id',
            field=models.IntegerField(default=0),
        ),
    ]