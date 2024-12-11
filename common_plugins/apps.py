from django.apps import AppConfig


class CommonPluginsConfig(AppConfig):
    name = "common_plugins"

    # TODO: remove this monkey patch if InlineCascadeElement has order by id
    def ready(self):
        from cmsplugin_cascade.models import CascadeElement

        # Define a function to be used as the replacement for copy_relations
        def custom_copy_relations(self, oldinstance):
            def init_element(inline_element):
                inline_element.pk = None
                inline_element.cascade_element = self
                inline_element.save()

            for inline_element in oldinstance.inline_elements.all().order_by("id"):
                init_element(inline_element)
            for sortinline_element in oldinstance.sortinline_elements.all():
                init_element(sortinline_element)

        # Monkey-patch the copy_relations method of the CascadeElement model
        CascadeElement.copy_relations = custom_copy_relations