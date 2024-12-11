# Generated by Django 3.1.14 on 2023-06-19 19:16

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pinogy_testimonials', '0012_googleplace_googlereviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='googlereviews',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2023, 6, 19, 19, 16, 31, 696386, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='googlereviews',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='googlereviews',
            name='place',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='place_review', to='pinogy_testimonials.googleplace'),
        ),
        migrations.AddField(
            model_name='googlereviews',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]
