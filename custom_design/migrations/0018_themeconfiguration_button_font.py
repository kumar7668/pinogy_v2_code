# Generated by Django 3.2.19 on 2024-04-18 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_design', '0017_alter_themeconfiguration_font_alignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='themeconfiguration',
            name='button_font',
            field=models.CharField(default='"Open Sans", Arial, sans-serif', max_length=100),
        ),
    ]