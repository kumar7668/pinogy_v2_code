# Generated by Django 3.1.14 on 2023-04-26 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('common_plugins', '0010_merge_20230425_1828'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscribePluginModel',
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
