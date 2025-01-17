# Generated by Django 3.1.14 on 2023-03-16 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiPetTypePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.TextField(blank=True, default=None, null=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('file_name', models.CharField(blank=True, default=None, max_length=300, null=True)),
                ('file_extension', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='file_extension')),
                ('file_image', models.ImageField(upload_to='ap_media')),
                ('file_id', models.IntegerField(blank=True, default=0, verbose_name='remote file ID')),
                ('alt', models.CharField(blank=True, default=None, max_length=300, null=True)),
                ('width', models.IntegerField(blank=True, default=0, verbose_name='Image file width')),
                ('height', models.IntegerField(blank=True, default=0, verbose_name='Image file height')),
                ('order_updated_at', models.DateTimeField(auto_now_add=True)),
                ('pet_type_id', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
    ]
