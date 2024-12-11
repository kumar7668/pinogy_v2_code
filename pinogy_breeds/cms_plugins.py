from cms.plugin_pool import plugin_pool
from cmsplugin_cascade.plugin_base import CascadePluginBase
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import gettext_lazy as _
from django.http import Http404
from common_plugins import utils
from pos_api.pos_client import PWAPI
from django.core.cache import cache

from common_plugins.forms import CollectionForm
from pinogy_breeds.forms import BreedTypeListPluginForm, BreedDetailPluginForm
from pinogy_breeds.pos_api import BreedList, PetTypeList, Breed, BreedDetail
from .models import BreedDetailPluginModel

@plugin_pool.register_plugin
class BreedTypeListPlugin(CascadePluginBase):
    """
    Plugin to display breeds of all available pet types
    """

    name = "Breed Types List"
    module = "Pinogy"
    form = BreedTypeListPluginForm
    change_form_template = "custom_design/admin/change_form.html"
    render_template = "pinogy_breeds/plugins/breed_type_list.html"
    cache = False

    def get_render_template(self, context, instance, placeholder):
        return instance.glossary.get("template_type") or "pinogy_breeds/plugins/breed_type_list.html"
    
    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['collection_form'] = CollectionForm
        client = PWAPI()
        store_data = utils.get_stores_data(client=client)
        request = context["request"]
        default_store_id = None
        if len(store_data) > 0:
            default_store_id = store_data[0].get('id',None)

        store_id = request.session.get('store_location_id') or \
            request.COOKIES.get('store_location_id') or default_store_id
        
        context['location_id'] = store_id
        
        breeds_pet_type = instance.glossary.get("breeds_pet_type")
        pet_type_slug = context.get('selected_pet_type_slug', None)  # Coming from BreedsView
        
        breed_obj = BreedList()
        breed_list = breed_obj.get_breed_list(pet_type_slug, breeds_pet_type)
        
        if instance.glossary.get("show_tabs_pet_type") == 'True':
            pet_types_obj = PetTypeList()
            pet_types_list = pet_types_obj.get_pet_type_list(breeds_pet_type)
            context["pet_types_list"] = pet_types_list
        
        context['breed_list'] = breed_list
        return context


@plugin_pool.register_plugin
class BreedDetailPlugin(CascadePluginBase):
    """
    Plugin to display breeds Detail
    """

    name = "Breed Detail"
    module = "Pinogy"
    form = BreedDetailPluginForm
    model = BreedDetailPluginModel
    change_form_template = "pinogy_breeds/forms/breed_detail.html"
    render_template = "pinogy_breeds/plugins/breed_detail.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['collection_form'] = CollectionForm
        request = context["request"]
        client = PWAPI()
        store_data = utils.get_stores_data(client=client)
        default_store_id = None
        if len(store_data) > 0:
            default_store_id = store_data[0].get('id',None)

        store_id = request.session.get('store_location_id') or \
            request.COOKIES.get('store_location_id') or default_store_id
        
        context['location_id'] = store_id
        
        context['shopwindow_enable'] = utils.is_shopwindow_enable(store_id)
        # Breed data comes from BreedView
        # these plugin needs to be added in breed detail page apphook
        # to use this plugin in any other page needs to write code for fetch the data 
        breed_data: Breed = context.get('selected_breed_data', None)  # Coming from BreedsView
        if breed_data:
            # breed_metric_info data is only used for layout3 traits design
            # Each metric value is divided by 2 to fit into five blocks
            # The quotient (quo) will determine the number of full blocks
            # The remainder (rem) will determine if there's a half block (50% progress bar)
            # rem_val will determine the number of empty blocks (0% progress bar)
            metrics_info = []
            for metrics in breed_data.metrics:
                val = metrics.value
                quo = int(val/2)
                rem = int(val%2)
                rem_val = 5-(quo+rem)
                metrics_info.append((list(range(quo)),list(range(rem)),list(range(rem_val)),metrics.name))
            
            context['breed_metrics_info'] = metrics_info
            context['breed'] = breed_data
            context['breed_name'] = breed_data.name
            context['breed_traits'] = breed_data.metrics
            context['breed_notes'] = breed_data.notes
            context['badges_length'] = len(breed_data.badge_images)
            #context['selected_plural'] = breed_data.pet_type.selected_plural.get(breed_data.pet_type.name,'')
        
        # update message 
        # Replaced the placeholder '{breed_name}' in the message with the actual breed name
        message = instance.glossary.get('message',"")

        if message is not None and message != '':
            breed_name = breed_data.name
            breed_name = breed_name[:-1].title() if breed_name.endswith('s') else breed_name.title()
            message = message.replace("{breed_name}", breed_name)
            instance.glossary['message'] = message

        return context