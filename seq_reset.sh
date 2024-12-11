#!/bin/sh

python manage.py sqlsequencereset admin | python manage.py dbshell
python manage.py sqlsequencereset aldryn_apphooks_config | python manage.py dbshell
python manage.py sqlsequencereset auth | python manage.py dbshell
python manage.py sqlsequencereset bootstrap4_alerts | python manage.py dbshell
python manage.py sqlsequencereset bootstrap4_badge | python manage.py dbshell
python manage.py sqlsequencereset bootstrap4_card | python manage.py dbshell
python manage.py sqlsequencereset bootstrap4_carousel | python manage.py dbshell
python manage.py sqlsequencereset bootstrap4_collapse | python manage.py dbshell
python manage.py sqlsequencereset bootstrap4_content | python manage.py dbshell
python manage.py sqlsequencereset bootstrap4_grid | python manage.py dbshell
echo "Line 11 `date`"
python manage.py sqlsequencereset bootstrap4_jumbotron | python manage.py dbshell
python manage.py sqlsequencereset bootstrap4_link | python manage.py dbshell
python manage.py sqlsequencereset bootstrap4_listgroup | python manage.py dbshell
python manage.py sqlsequencereset bootstrap4_media | python manage.py dbshell
python manage.py sqlsequencereset bootstrap4_picture | python manage.py dbshell
python manage.py sqlsequencereset bootstrap4_tabs | python manage.py dbshell
python manage.py sqlsequencereset bootstrap4_utilities | python manage.py dbshell
python manage.py sqlsequencereset carousel_plugins | python manage.py dbshell
python manage.py sqlsequencereset clipboard | python manage.py dbshell
python manage.py sqlsequencereset cms | python manage.py dbshell
echo "Line 21 `date`"
python manage.py sqlsequencereset cmsplugin_cascade | python manage.py dbshell
python manage.py sqlsequencereset colorfield | python manage.py dbshell
python manage.py sqlsequencereset common_plugins | python manage.py dbshell
python manage.py sqlsequencereset compressor | python manage.py dbshell
python manage.py sqlsequencereset contenttypes | python manage.py dbshell
python manage.py sqlsequencereset custom_design | python manage.py dbshell
python manage.py sqlsequencereset django_db_logger | python manage.py dbshell
python manage.py sqlsequencereset django_select2 | python manage.py dbshell
python manage.py sqlsequencereset djangocms_admin_style | python manage.py dbshell
python manage.py sqlsequencereset djangocms_blog | python manage.py dbshell
echo "Line 31 `date`"
python manage.py sqlsequencereset djangocms_bootstrap4 | python manage.py dbshell
python manage.py sqlsequencereset djangocms_file | python manage.py dbshell
python manage.py sqlsequencereset djangocms_googlemap | python manage.py dbshell
python manage.py sqlsequencereset djangocms_icon | python manage.py dbshell
python manage.py sqlsequencereset djangocms_link | python manage.py dbshell
python manage.py sqlsequencereset djangocms_picture | python manage.py dbshell
python manage.py sqlsequencereset djangocms_snippet | python manage.py dbshell
python manage.py sqlsequencereset djangocms_style | python manage.py dbshell
python manage.py sqlsequencereset djangocms_text_ckeditor | python manage.py dbshell
python manage.py sqlsequencereset djangocms_video | python manage.py dbshell
echo "Line 41 `date`"
python manage.py sqlsequencereset easy_thumbnails | python manage.py dbshell
python manage.py sqlsequencereset extra_fields | python manage.py dbshell
python manage.py sqlsequencereset filer | python manage.py dbshell
python manage.py sqlsequencereset humanize | python manage.py dbshell
python manage.py sqlsequencereset menus | python manage.py dbshell
python manage.py sqlsequencereset messages | python manage.py dbshell
python manage.py sqlsequencereset meta | python manage.py dbshell
python manage.py sqlsequencereset parler | python manage.py dbshell
python manage.py sqlsequencereset pinogy_app | python manage.py dbshell
python manage.py sqlsequencereset pinogy_breeds | python manage.py dbshell
echo "Line 51 `date`"
python manage.py sqlsequencereset pinogy_cache | python manage.py dbshell
python manage.py sqlsequencereset pinogy_pet | python manage.py dbshell
python manage.py sqlsequencereset pinogy_redirect | python manage.py dbshell
python manage.py sqlsequencereset pinogy_shop | python manage.py dbshell
python manage.py sqlsequencereset pinogy_site_config | python manage.py dbshell
python manage.py sqlsequencereset pinogy_testimonials | python manage.py dbshell
python manage.py sqlsequencereset pos_api | python manage.py dbshell
python manage.py sqlsequencereset recaptcha2 | python manage.py dbshell
python manage.py sqlsequencereset recaptcha3 | python manage.py dbshell
python manage.py sqlsequencereset robots | python manage.py dbshell
echo "Line 61 `date`"
python manage.py sqlsequencereset segmentation | python manage.py dbshell
python manage.py sqlsequencereset sekizai | python manage.py dbshell
python manage.py sqlsequencereset sessions | python manage.py dbshell
python manage.py sqlsequencereset sharable | python manage.py dbshell
python manage.py sqlsequencereset sitemaps | python manage.py dbshell
python manage.py sqlsequencereset sites | python manage.py dbshell
python manage.py sqlsequencereset solo | python manage.py dbshell
python manage.py sqlsequencereset sortedm2m | python manage.py dbshell
python manage.py sqlsequencereset staticfiles | python manage.py dbshell
python manage.py sqlsequencereset taggit | python manage.py dbshell
echo "Line 71 `date`"
python manage.py sqlsequencereset taggit_autosuggest | python manage.py dbshell
python manage.py sqlsequencereset treebeard | python manage.py dbshell
echo "Done at `date`"
