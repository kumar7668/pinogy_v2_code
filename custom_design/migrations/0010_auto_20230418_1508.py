# Generated by Django 3.1.14 on 2023-04-18 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_design', '0009_auto_20221128_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='themeconfiguration',
            name='general_font',
            field=models.CharField(default='"Open Sans", Arial, sans-serif', max_length=100),
        ),
        migrations.AlterField(
            model_name='themeconfiguration',
            name='heading_font',
            field=models.CharField(default='"Open Sans", Arial, sans-serif', max_length=100),
        ),
    ]