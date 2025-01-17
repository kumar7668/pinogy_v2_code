# Generated by Django 2.1.1 on 2022-04-21 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinogy_testimonials', '0009_auto_20220413_0214'),
    ]

    operations = [
        
        migrations.AlterField(
            model_name='testimonialcarouselpluginmodel',
            name='available_template',
            field=models.CharField(blank=True, choices=[('testimonials_new/plugins/testimonial_carousel/testimonial_carousel.html', 'Default'), ('testimonials_new/plugins/testimonial_carousel/images_with_text_right.html', 'Image with text in right'), ('testimonials_new/plugins/testimonial_carousel/image_text_right_curve_corner.html', 'Image with text in right and curve corner'), ('testimonials_new/plugins/testimonial_carousel/testimonial_card_design.html', 'Card Layout')], default='testimonials_new/plugins/testimonial_carousel/testimonial_carousel.html', max_length=256, null=True, verbose_name='Available Template'),
        ),

    ]
