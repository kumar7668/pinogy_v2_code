# Generated by Django 3.1.14 on 2022-12-13 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carousel_plugins', '0003_delete_petcarouselpluginmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_content', models.FileField(upload_to='ap_media')),
                ('file_name', models.CharField(blank=True, default=None, max_length=1000, null=True)),
                ('file_extension', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='file_extension')),
                ('brand_id', models.IntegerField(default=-1)),
                ('brand_image_id', models.IntegerField(default=-1)),
            ],
        ),
    ]
