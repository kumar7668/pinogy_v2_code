# Generated by Django 2.1.1 on 2022-03-31 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinogy_testimonials', '0006_auto_20200810_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonialcarouselpluginmodel',
            name='available_template',
            field=models.CharField(blank=True, choices=[('testimonials_new/plugins/testimonial_carousel/testimonial_carousel.html', 'Default'), ('testimonials_new/plugins/testimonial_carousel/images_with_text_right.html', 'Image with text in right')], default='testimonials_new/plugins/testimonial_carousel/testimonial_carousel.html', max_length=256, null=True, verbose_name='Available Template'),
        ),
    ]
