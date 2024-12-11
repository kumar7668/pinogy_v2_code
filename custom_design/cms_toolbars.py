from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK
from cms.toolbar.items import Break, SubMenu
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse, reverse
from django.utils.translation import ugettext_lazy as _


class ThemeToolbar(CMSToolbar):
    """
    Added theme change in django-cms toolbar.
    """

    def populate(self):
        admin_menu = self.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER)

        position = admin_menu.get_alphabetical_insert_position(
            _("Site Configuration"), SubMenu
        )

        if not position:
            position = admin_menu.find_first(Break, identifier=ADMINISTRATION_BREAK) + 1
            admin_menu.add_break("custom-break", position=position)

        menu = admin_menu.get_or_create_menu(
            "pinogy_site_config-menu", _("Site Configuration"), position=position
        )

        menu.add_sideframe_item(
            name="Template Select",
            url=admin_reverse("custom_design_templateconfig_changelist"),
        )

        menu.add_link_item(
            name="Theme Configuration",
            url=reverse("theme-change"),
        )

        menu.add_sideframe_item(
            name="Clear Cache",
            url=reverse("clearcache_admin"),
        )

        menu.add_break()

        menu.add_sideframe_item(
            _('Site configuration'), 
            url=admin_reverse('pinogy_site_config_siteconfig_changelist'),
        )

toolbar_pool.register(ThemeToolbar)
