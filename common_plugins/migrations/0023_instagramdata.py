# Generated by Django 3.2.19 on 2024-04-03 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common_plugins', '0022_instagramfeedpluginmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=255, unique=True)),
                ('permalink', models.URLField()),
                ('media_url', models.CharField(max_length=500)),
                ('caption', models.CharField(blank=True, max_length=256, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('plugin', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='common_plugins.instagramfeedpluginmodel')),
            ],
        ),
    ]