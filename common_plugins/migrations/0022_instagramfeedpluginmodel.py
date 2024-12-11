# Generated by Django 3.2.19 on 2024-04-01 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('common_plugins', '0021_auto_20240319_0501'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramFeedPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='common_plugins_instagramfeedpluginmodel', serialize=False, to='cms.cmsplugin')),
                ('access_token', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
