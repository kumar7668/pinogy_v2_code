from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cmsplugin_cascade.plugin_base import CascadePluginBase

from pinogy_app.models import Plugin1Model, SiteMapModel


@plugin_pool.register_plugin
class SamplePlugin(CMSPluginBase):
    name = "Sample Plugin"
    module = "Testing"
    render_template = "hello_plugin.html"
    model = CMSPlugin
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context["key"] = "value"
        return context


@plugin_pool.register_plugin
class DemoPlugin(CascadePluginBase):
    name = "Demo Plugin"
    module = "Testing"
    render_template = "hello_plugin.html"
    model = Plugin1Model

    def render(self, context, instance, placeholder):
        if instance.is_show:
            self.show()
        else:
            self.hide()
        return super().render(context, instance, placeholder)

    def show(self):
        return "show"

    def hide(self):
        return "hide"

@plugin_pool.register_plugin
class SiteMapPlugin(CMSPluginBase):
    module = 'Pinogy'
    model = SiteMapModel
    name = 'Site Map Plugin'
    cache = True
    render_template = 'pinogy_app/plugins/sitemap.html'