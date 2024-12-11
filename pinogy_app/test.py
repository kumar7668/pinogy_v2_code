from cms.api import add_plugin
from cms.models import Placeholder
from cms.plugin_rendering import ContentRenderer
from django.test import TestCase
from django.test.client import RequestFactory

from .cms_plugins import DemoPlugin, SamplePlugin


class SamplePluginTests(TestCase):
    def test_plugin_context(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(
            placeholder,
            SamplePlugin,
            "en",
        )
        plugin_instance = model_instance.get_plugin_class_instance()
        context = plugin_instance.render({}, model_instance, None)
        self.assertIn("key", context)
        self.assertEqual(context["key"], "value")

    def test_plugin_html(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(
            placeholder,
            SamplePlugin,
            "en",
        )
        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(model_instance, {})
        self.assertIn("<strong>Test</strong>", html)


class DemoPluginTests(TestCase):
    def test_plugin_hide(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(
            placeholder,
            DemoPlugin,
            "en",
        )
        plugin_instance = model_instance.get_plugin_class_instance()
        _ = plugin_instance.render({}, model_instance, None)

    def test_plugin_show(self):
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(placeholder, DemoPlugin, "en", **{"is_show": True})
        plugin_instance = model_instance.get_plugin_class_instance()
        _ = plugin_instance.render({}, model_instance, None)
