# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinogy_testimonials', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonialcarouselpluginmodel',
            name='share_button_text',
            field=models.CharField(default='Share your own pet story!', help_text='Provide your own share button text', max_length=255),
        ),
        migrations.AddField(
            model_name='testimonialquotespluginmodel',
            name='share_button_text',
            field=models.CharField(default='Share your own pet story!', help_text='Provide your own share button text', max_length=255),
        ),
    ]
