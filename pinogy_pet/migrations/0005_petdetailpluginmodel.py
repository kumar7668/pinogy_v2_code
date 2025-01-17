# Generated by Django 3.2.19 on 2024-07-25 11:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('pinogy_pet', '0004_apipetadcard_pet_type_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='PetDetailPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='+', serialize=False, to='cms.cmsplugin')),
                ('glossary', models.JSONField(blank=True, default=dict)),
                ('promob_image', models.ImageField(blank=True, default=None, null=True, upload_to='background', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'webp'])])),
                ('button_data', models.JSONField(blank=True, default=None, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
