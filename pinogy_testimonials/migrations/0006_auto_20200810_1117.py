# Generated by Django 2.1.1 on 2020-08-10 11:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinogy_testimonials', '0005_auto_20200421_0721'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonialcarouselpluginmodel',
            name='display_with_star',
            field=models.BooleanField(default=True, help_text='Display star as rate of testimonial.'),
        ),
        migrations.AddField(
            model_name='testimonialcarouselpluginmodel',
            name='displayed_count',
            field=models.PositiveIntegerField(default=3, help_text='How many testimonials displayed on carousel?', validators=[django.core.validators.MaxValueValidator(10)], verbose_name='displayed count'),
        ),
        migrations.AddField(
            model_name='testimonialcarouselpluginmodel',
            name='set_padding',
            field=models.BooleanField(default=True, help_text='Set padding for testimonial item.'),
        ),
    ]
