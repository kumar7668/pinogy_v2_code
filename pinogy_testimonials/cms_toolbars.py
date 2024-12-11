# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK
from cms.toolbar.items import Break, SubMenu
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse

from .models import Testimonial


@toolbar_pool.register
class TestimonialsToolbar(CMSToolbar):
    watch_models = (Testimonial, )

    def populate(self):
        admin_menu = self.toolbar.get_or_create_menu(
            ADMIN_MENU_IDENTIFIER)

        position = admin_menu.get_alphabetical_insert_position(
            _('Testimonials'), SubMenu)

        if not position:
            position = admin_menu.find_first(
                Break, identifier=ADMINISTRATION_BREAK) + 1
            admin_menu.add_break('custom_break', position=position)

        menu = admin_menu.get_or_create_menu('testimonials-app',
            _('Testimonials'), position=position)

        if self.request.user.has_perm('pinogy_testimonials.change_testimonial'):
            menu.add_sideframe_item(_('Testimonials'),
                url=admin_reverse('pinogy_testimonials_testimonial_changelist'))

        if self.request.user.has_perm('pinogy_testimonials.add_testimonial'):
            menu.add_modal_item(_('Add new testimonial'),
                url=admin_reverse('pinogy_testimonials_testimonial_add'))
            
        if self.request.user.has_perm('pinogy_testimonials.change_googlereviews'):
            menu.add_sideframe_item(_('Google Reviews'),
                url=admin_reverse('pinogy_testimonials_googlereviews_changelist'))
