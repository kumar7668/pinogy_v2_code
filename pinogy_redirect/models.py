from django.db import models
from django.contrib.sites.models import Site
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, ugettext

from parler.models import TranslatableModel, TranslatedFields

from .managers import RedirectApplicationManager, PathLogManager, NotFoundLogManager
from .utils import update_new_path


class Redirect(TranslatableModel):
    site = models.ForeignKey(
        Site, related_name='pinogy_redirect_redirect_set', on_delete=models.CASCADE)
    old_path = models.CharField(
        _('redirect from'), max_length=200, db_index=True,
        help_text=_(
            "This should be an absolute path, excluding the domain name. "
            "Example: '/events/search/'."
        ),
    )
    translations = TranslatedFields(
        new_path=models.CharField(
            _('redirect to'), max_length=200, blank=True,
            help_text=_(
                "This can be either an absolute path (as above) or a full URL "
                "starting with 'http://'."
            ),
        ),
    )

    class Meta:
        verbose_name = _('redirect')
        verbose_name_plural = _('redirects')
        unique_together = (('site', 'old_path'),)
        ordering = ('old_path',)

    def __unicode__(self):
        new_paths = ', '.join([
            '{}:{}'.format(t.language_code, t.new_path)
            for t in self.translations.all()
        ])
        if not new_paths:
            new_paths = ugettext('None')
        return "{} ---> {}".format(self.old_path or 'None', new_paths)


class RedirectApplication(models.Model):

    APP_HOOKS_FOR_UPDATE = ('PetDetailApphook',)

    site = models.ForeignKey(
        Site, related_name='pinogy_redirect_redirectapp_set', on_delete=models.CASCADE)
    old_path_application = models.CharField(
        _('redirect from application'), max_length=200, db_index=True,
        help_text=_(
            "This should be an absolute path, excluding the domain name. "
            "Example: '/events/search/'."
        ),
    )
    page_application = models.ForeignKey(
        "cms.Page", on_delete=models.CASCADE, null=False,
        help_text=_(
            "Redirect from application path will be redirected to hook of this Application"
        ),
    )
    extra_part = models.CharField(
        _('Extra path'), max_length=200, db_index=True, blank=True, default='',
        help_text=_("This path will be added to selected Application Hook"),
    )

    objects = RedirectApplicationManager()

    class Meta:
        verbose_name = _('redirect_application')
        verbose_name_plural = _('redirect_apps')
        unique_together = (('site', 'old_path_application'),)
        ordering = ('-pk',)

    @property
    def default_path(self):
        result = self.page_application.get_absolute_url()
        if self.extra_part != '':
            result = result[:-1] + self.extra_part
        return result

    @property
    def is_except_path_update(self):
        return self.page_application.application_urls in RedirectApplication.APP_HOOKS_FOR_UPDATE

    def get_new_path(self, old_path):
        new_path = self.default_path
        if self.is_except_path_update:
            new_path = update_new_path(old_path, new_path)

        return new_path


class PathLog(models.Model):

    path = models.CharField(
        max_length=200, db_index=True, blank=True, default='broken_link', unique=True,
        help_text=_("Logged request path"),
    )

    objects = PathLogManager()

    class Meta:
        verbose_name = '404 Log'
        verbose_name_plural = '404 Logs'


class NotFoundLog(models.Model):

    logged_at = models.DateTimeField(default=timezone.now)
    path_log = models.ForeignKey(PathLog, on_delete=models.CASCADE, null=False, related_name='logs')

    objects = NotFoundLogManager()
