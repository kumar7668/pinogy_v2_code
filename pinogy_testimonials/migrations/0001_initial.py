# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image
import django.core.validators
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('filer', '0002_auto_20150606_2003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_published', models.BooleanField(default=False, help_text='Check this box to publish this testimonial on the site.', verbose_name='published?')),
                ('is_featured', models.BooleanField(default=False, help_text='Check this box to feature this testimonial on the site.', verbose_name='featured?')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('photo', filer.fields.image.FilerImageField(default=None, to='filer.Image', blank=True, help_text='Share a photo of your pet. (JPG, PNG accepted up to 2MBs)', null=True, verbose_name='your pet photo', on_delete=django.db.models.deletion.DO_NOTHING)),
            ],
            options={
                'verbose_name': 'testimonial',
                'verbose_name_plural': 'testimonials',
            },
        ),
        migrations.CreateModel(
            name='TestimonialCarouselPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='+', primary_key=True, serialize=False, to='cms.CMSPlugin', on_delete=django.db.models.deletion.DO_NOTHING)),
                ('max_testimonials', models.PositiveIntegerField(default=5, help_text='How many should be shown (up to 15)?', verbose_name='max. testimonials', validators=[django.core.validators.MaxValueValidator(15)])),
                ('restrict_to_featured', models.BooleanField(default=False, help_text='Check to show only featured testimonials.')),
                ('restrict_to_language', models.BooleanField(default=False, help_text='Check to only show testimonials in viewer\u2019s langauge.')),
                ('image_restriction', models.PositiveSmallIntegerField(default=0, help_text='Should there be any restriction for images?.', choices=[(0, 'show testimonials with or without images'), (1, 'only show testimonials with images'), (2, 'only show testimonials without images')])),
                ('show_add_option', models.BooleanField(default=True, help_text='Check to show option to add a new testimonial.')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='TestimonialFormPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='+', primary_key=True, serialize=False, to='cms.CMSPlugin', on_delete=django.db.models.deletion.DO_NOTHING)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='TestimonialQuotesPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='+', primary_key=True, serialize=False, to='cms.CMSPlugin', on_delete=django.db.models.deletion.DO_NOTHING)),
                ('max_testimonials', models.PositiveIntegerField(default=5, help_text='How many should be shown (up to 15)?', verbose_name='max. testimonials', validators=[django.core.validators.MaxValueValidator(15)])),
                ('restrict_to_featured', models.BooleanField(default=False, help_text='Check to show only featured testimonials.')),
                ('restrict_to_language', models.BooleanField(default=False, help_text='Check to only show testimonials in viewer\u2019s langauge.')),
                ('image_restriction', models.PositiveSmallIntegerField(default=0, help_text='Should there be any restriction for images?.', choices=[(0, 'show testimonials with or without images'), (1, 'only show testimonials with images'), (2, 'only show testimonials without images')])),
                ('show_add_option', models.BooleanField(default=True, help_text='Check to show option to add a new testimonial.')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='TestimonialTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('subject', models.CharField(default='', help_text='Enter a short headline for your story.', max_length=255, verbose_name='headline')),
                ('body', models.TextField(default='', help_text='Enter your story here.', verbose_name='your story')),
                ('display_name', models.CharField(default='', help_text='Enter the name that you would like this story to be attributed to. (E.g., \u201cThe Smith family\u201d or \u201cJ. Doe\u201d)', max_length=255, verbose_name='display name')),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='pinogy_testimonials.Testimonial', null=True, on_delete=django.db.models.deletion.DO_NOTHING)),
            ],
            options={
                'managed': True,
                'db_table': 'pinogy_testimonials_testimonial_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'testimonial Translation',
            },
        ),
        migrations.AlterUniqueTogether(
            name='testimonialtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
