# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TestimonialTranslation'
        db.create_table(u'pinogy_testimonials_testimonial_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255)),
            ('body', self.gf('django.db.models.fields.TextField')(default=u'')),
            ('display_name', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255)),
            (u'master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['pinogy_testimonials.Testimonial'])),
        ))
        db.send_create_signal(u'pinogy_testimonials', ['TestimonialTranslation'])

        # Adding unique constraint on 'TestimonialTranslation', fields ['language_code', u'master']
        db.create_unique(u'pinogy_testimonials_testimonial_translation', ['language_code', u'master_id'])

        # Deleting field 'TestimonialCarouselPluginModel.restrict_to_images'
        db.delete_column(u'pinogy_testimonials_testimonialcarouselpluginmodel', 'restrict_to_images')

        # Adding field 'TestimonialCarouselPluginModel.restrict_to_language'
        db.add_column(u'pinogy_testimonials_testimonialcarouselpluginmodel', 'restrict_to_language',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TestimonialCarouselPluginModel.image_restriction'
        db.add_column(u'pinogy_testimonials_testimonialcarouselpluginmodel', 'image_restriction',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'TestimonialQuotesPluginModel.restrict_to_images'
        db.delete_column(u'pinogy_testimonials_testimonialquotespluginmodel', 'restrict_to_images')

        # Adding field 'TestimonialQuotesPluginModel.restrict_to_language'
        db.add_column(u'pinogy_testimonials_testimonialquotespluginmodel', 'restrict_to_language',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TestimonialQuotesPluginModel.image_restriction'
        db.add_column(u'pinogy_testimonials_testimonialquotespluginmodel', 'image_restriction',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Testimonial.body'
        db.delete_column(u'pinogy_testimonials_testimonial', 'body')

        # Deleting field 'Testimonial.display_name'
        db.delete_column(u'pinogy_testimonials_testimonial', 'display_name')

        # Deleting field 'Testimonial.subject'
        db.delete_column(u'pinogy_testimonials_testimonial', 'subject')


    def backwards(self, orm):
        # Removing unique constraint on 'TestimonialTranslation', fields ['language_code', u'master']
        db.delete_unique(u'pinogy_testimonials_testimonial_translation', ['language_code', u'master_id'])

        # Deleting model 'TestimonialTranslation'
        db.delete_table(u'pinogy_testimonials_testimonial_translation')

        # Adding field 'TestimonialCarouselPluginModel.restrict_to_images'
        db.add_column(u'pinogy_testimonials_testimonialcarouselpluginmodel', 'restrict_to_images',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'TestimonialCarouselPluginModel.restrict_to_language'
        db.delete_column(u'pinogy_testimonials_testimonialcarouselpluginmodel', 'restrict_to_language')

        # Deleting field 'TestimonialCarouselPluginModel.image_restriction'
        db.delete_column(u'pinogy_testimonials_testimonialcarouselpluginmodel', 'image_restriction')

        # Adding field 'TestimonialQuotesPluginModel.restrict_to_images'
        db.add_column(u'pinogy_testimonials_testimonialquotespluginmodel', 'restrict_to_images',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'TestimonialQuotesPluginModel.restrict_to_language'
        db.delete_column(u'pinogy_testimonials_testimonialquotespluginmodel', 'restrict_to_language')

        # Deleting field 'TestimonialQuotesPluginModel.image_restriction'
        db.delete_column(u'pinogy_testimonials_testimonialquotespluginmodel', 'image_restriction')

        # Adding field 'Testimonial.body'
        db.add_column(u'pinogy_testimonials_testimonial', 'body',
                      self.gf('django.db.models.fields.TextField')(default=u''),
                      keep_default=False)

        # Adding field 'Testimonial.display_name'
        db.add_column(u'pinogy_testimonials_testimonial', 'display_name',
                      self.gf('django.db.models.fields.CharField')(default=u'', max_length=255),
                      keep_default=False)

        # Adding field 'Testimonial.subject'
        db.add_column(u'pinogy_testimonials_testimonial', 'subject',
                      self.gf('django.db.models.fields.CharField')(default=u'', max_length=255),
                      keep_default=False)


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'filer.file': {
            'Meta': {'object_name': 'File'},
            '_file_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'all_files'", 'null': 'True', 'to': u"orm['filer.Folder']"}),
            'has_all_mandatory_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'original_filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'owned_files'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_filer.file_set+'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'sha1': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '40', 'blank': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'filer.folder': {
            'Meta': {'ordering': "(u'name',)", 'unique_together': "((u'parent', u'name'),)", 'object_name': 'Folder'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'filer_owned_folders'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': u"orm['filer.Folder']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'filer.image': {
            'Meta': {'object_name': 'Image'},
            '_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            '_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'default_alt_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'default_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'file_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['filer.File']", 'unique': 'True', 'primary_key': 'True'}),
            'must_always_publish_author_credit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'must_always_publish_copyright': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject_location': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'pinogy_testimonials.testimonial': {
            'Meta': {'object_name': 'Testimonial'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['filer.Image']", 'null': 'True', 'blank': 'True'})
        },
        u'pinogy_testimonials.testimonialcarouselpluginmodel': {
            'Meta': {'object_name': 'TestimonialCarouselPluginModel'},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'+'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['cms.CMSPlugin']"}),
            'image_restriction': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'max_testimonials': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5'}),
            'restrict_to_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'restrict_to_language': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_add_option': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'pinogy_testimonials.testimonialformpluginmodel': {
            'Meta': {'object_name': 'TestimonialFormPluginModel'},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'+'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['cms.CMSPlugin']"})
        },
        u'pinogy_testimonials.testimonialquotespluginmodel': {
            'Meta': {'object_name': 'TestimonialQuotesPluginModel'},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'+'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['cms.CMSPlugin']"}),
            'image_restriction': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'max_testimonials': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5'}),
            'restrict_to_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'restrict_to_language': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_add_option': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'pinogy_testimonials.testimonialtranslation': {
            'Meta': {'unique_together': "[(u'language_code', u'master')]", 'object_name': 'TestimonialTranslation', 'db_table': "u'pinogy_testimonials_testimonial_translation'"},
            'body': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'display_name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            u'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['pinogy_testimonials.Testimonial']"}),
            'subject': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'})
        }
    }

    complete_apps = ['pinogy_testimonials']