# Generated by Django 3.2.19 on 2024-07-20 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_plugins', '0031_alter_external_links_ext_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='external_links',
            name='internal_link_id',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
