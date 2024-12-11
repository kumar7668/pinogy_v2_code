from django.contrib import admin
from django.utils.html import format_html
from django.utils.http import urlencode
from parler.admin import TranslatableAdmin

from .forms import RedirectApplicationForm
from .models import Redirect, RedirectApplication, PathLog, NotFoundLog


class RedirectAdmin(TranslatableAdmin):
    list_display = ('old_path',)
    list_filter = ('site',)
    search_fields = ('old_path', 'new_path')
    radio_fields = {'site': admin.VERTICAL}

    def get_form(self, request, obj=None, **kwargs):
        form = super(RedirectAdmin, self).get_form(request, obj=None, **kwargs)
        site_field = form.base_fields['site']

        # the add and change links don't work anyway with admin.VERTICAL radio
        # fields
        site_field.widget.can_add_related = False
        site_field.widget.can_change_related = False

        # if there is only one site, select it by default
        if site_field.queryset.all().count() == 1:
            site_field.initial = site_field.queryset.get()
        return form


admin.site.register(Redirect, RedirectAdmin)


class RedirectApplicationAdmin(admin.ModelAdmin):
    form = RedirectApplicationForm
    list_display = ('old_path_application', 'page_application', 'site',)
    list_filter = ('site', 'page_application',)
    search_fields = ('old_path_application',)


admin.site.register(RedirectApplication, RedirectApplicationAdmin)


class NotFoundInline(admin.StackedInline):
    model = NotFoundLog


class PathLogAdmin(admin.ModelAdmin):
    inlines = (NotFoundInline,)
    list_display = ('path', 'first_log', 'last_log', 'log_count', 'resolve',)

    # table logic
    def get_ordering(self, request):
        return ('-last_log',)

    def has_change_permission(self, request, obj=None):
        return False

    # row items
    def first_log(self, obj):
        return obj.first_log

    first_log.short_description = 'Logged for the first time'
    first_log.admin_order_field = 'first_log'

    def last_log(self, obj):
        return obj.last_log

    last_log.short_description = 'Logged for the last time'
    last_log.admin_order_field = 'last_log'

    def log_count(self, obj):
        return obj.log_count

    log_count.short_description = 'Number of logs'
    log_count.admin_order_field = 'log_count'

    def resolve(self, obj):

        def get_button_tag(href, name, field):
            return '<a class="button" href="{}?{}">{}</a>'.format(href, urlencode({field: obj.path}), name)

        # TODO add after app redirect test
        #                 get_button_tag(href='/en/admin/pinogy_redirect/redirectapplication/add/',
        #                                name='Redirect to App', field='old_path_application')
        return format_html(
            '{}'.format(
                get_button_tag(href='/en/admin/pinogy_redirect/redirect/add/',
                               name='Redirect to Page', field='old_path')
            )
        )

    resolve.short_description = 'Resolve with'
    resolve.allow_tags = True


admin.site.register(PathLog, PathLogAdmin)