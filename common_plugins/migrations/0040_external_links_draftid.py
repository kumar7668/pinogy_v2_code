# Generated by Django 3.2.19 on 2024-09-24 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_plugins', '0039_auto_20240924_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='external_links',
            name='draftId',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
