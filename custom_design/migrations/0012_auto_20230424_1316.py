# Generated by Django 3.1.14 on 2023-04-24 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_design', '0011_auto_20230421_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='themeconfiguration',
            name='image_radius',
            field=models.CharField(default='0', max_length=100),
        ),
    ]
