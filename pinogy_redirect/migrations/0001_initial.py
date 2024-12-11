# Generated by Django 3.1.14 on 2023-06-09 10:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import parler.fields
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='PathLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(blank=True, db_index=True, default='broken_link', help_text='Logged request path', max_length=200, unique=True)),
            ],
            options={
                'verbose_name': '404 Log',
                'verbose_name_plural': '404 Logs',
            },
        ),
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_path', models.CharField(db_index=True, help_text="This should be an absolute path, excluding the domain name. Example: '/events/search/'.", max_length=200, verbose_name='redirect from')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pinogy_redirect_redirect_set', to='sites.site')),
            ],
            options={
                'verbose_name': 'redirect',
                'verbose_name_plural': 'redirects',
                'ordering': ('old_path',),
                'unique_together': {('site', 'old_path')},
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='NotFoundLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logged_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('path_log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='pinogy_redirect.pathlog')),
            ],
        ),
        migrations.CreateModel(
            name='RedirectTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('new_path', models.CharField(blank=True, help_text="This can be either an absolute path (as above) or a full URL starting with 'http://'.", max_length=200, verbose_name='redirect to')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='pinogy_redirect.redirect')),
            ],
            options={
                'verbose_name': 'redirect Translation',
                'db_table': 'pinogy_redirect_redirect_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RedirectApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_path_application', models.CharField(db_index=True, help_text="This should be an absolute path, excluding the domain name. Example: '/events/search/'.", max_length=200, verbose_name='redirect from application')),
                ('extra_part', models.CharField(blank=True, db_index=True, default='', help_text='This path will be added to selected Application Hook', max_length=200, verbose_name='Extra path')),
                ('page_application', models.ForeignKey(help_text='Redirect from application path will be redirected to hook of this Application', on_delete=django.db.models.deletion.CASCADE, to='cms.page')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pinogy_redirect_redirectapp_set', to='sites.site')),
            ],
            options={
                'verbose_name': 'redirect_application',
                'verbose_name_plural': 'redirect_apps',
                'ordering': ('-pk',),
                'unique_together': {('site', 'old_path_application')},
            },
        ),
    ]
