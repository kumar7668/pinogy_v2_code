# Generated by Django 3.2.19 on 2024-08-08 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('pinogy_breeds', '0002_apibreedbadgephoto'),
    ]

    operations = [
        migrations.CreateModel(
            name='BreedDetailPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='+', serialize=False, to='cms.cmsplugin')),
                ('glossary', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
