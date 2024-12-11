# Generated by Django 3.2.19 on 2024-09-02 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('carousel_plugins', '0006_auto_20230616_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='GridPluginModel',
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
