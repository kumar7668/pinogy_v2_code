# Generated by Django 3.2.19 on 2024-07-12 09:13

from django.db import migrations, models

def migrate_data(apps, schema_editor):
    MyModel = apps.get_model('common_plugins', 'headerpluginmodel')
    for instance in MyModel.objects.all():
        if isinstance(instance.Header_external_quick_links, dict):
            # Convert dictionary to list
            instance.Header_external_quick_links = list(instance.Header_external_quick_links.items())
            instance.save()

class Migration(migrations.Migration):


    dependencies = [
        ('common_plugins', '0028_auto_20240627_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headerpluginmodel',
            name='Header_external_quick_links',
            field=models.JSONField(default=list),
        ),
        migrations.RunPython(migrate_data),
    ]
