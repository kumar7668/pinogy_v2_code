from django.urls import reverse, NoReverseMatch
from django.apps import apps
from cms.models import Page, TreeNode, Title
# from cms.utils.page import get_node
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.db import transaction
from cmsplugin_cascade.plugin_base import CascadePluginBase
from cmsplugin_cascade.mixins import WithInlineElementsMixin
from pinogy_testimonials.models import Testimonial
from common_plugins.models import PopupPluginModel, External_links
from common_plugins.forms import (
    BannerPluginForm,
    PopupPluginForm,
    FooterPluginForm,
    HeaderPluginForm,
    InfoBlockFirstPluginForm,
    InfoBlockSecondPluginForm,
    SliderPluginForm,
    StaticInfoBlockPluginForm,
    GalleryPluginForm,
    GalleryItemForm,
    GalleryItemInline,
    StaticInfoItemInline,
    CollectionForm,
    SubscribeUsForm,
    SubscribeUsPluginForm,
    UnSubscribeUsPluginForm,
    ServicesBlockPluginForm,
    ServiceItemInline,
    ContactUsInfoPluginForm,
    ContactUsPluginForm,
    FAQBlockPluginForm,
    FAQTabInline,
    FAQAccordionPluginForm,
    FAQItemInline,
    LocationContactNumberPluginForm,
    LocationSocialPluginForm,
    ShowHidePluginForm,
)
from custom_design.models import ThemeImages

from .models import (
    BannerPluginModel,
    CardCarouselModel,
    FooterPluginModel,
    HeaderPluginModel,
    InfoBlockFirstPluginModel,
    InfoBlockSecondPluginModel,
    SliderPluginModel,
    SubscribePluginModel,
    UnSubscribePluginModel,
    ContactUsInfoPluginModel,
    InstagramFeedPluginModel,
    TabsCompoPluginModel,
    TabItemCompoPluginModel,
)
from . import utils
from pos_api.pos_client import PWAPI
from datetime import datetime,date
from pinogy_shop.pos_api.product import ProductClient
from pinogy_shop.utils import get_country_list, get_country_regions
from common_plugins.utils import get_stores_data, int_to_base36, base36_to_int
from pinogy_shop.pos_api import CustomerClient
import json

@plugin_pool.register_plugin
class BannerPlugin(CascadePluginBase):
    name = "Banner"
    module = "Pinogy"
    model = BannerPluginModel
    form = BannerPluginForm
    render_template = "plugins/banner_plugin/banner_plugin_v2.html"
    change_form_template = "plugins/banner_plugin/banner_change_form.html"
    cache = False

    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        return super().render_change_form(request, context, add, change, form_url, obj)

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        # TODO: remove this since we are not using
        # Add button action link in context
        # if instance.glossary.get("first_button_internallink"):
        #     page = Page.objects.filter(
        #         id=instance.glossary.get("first_button_internallink", {}).get("pk")
        #     ).first()
        #     if page:
        #         context["first_btn_link"] = page.get_absolute_url()
        #     elif instance.glossary.get("first_button_link"):
        #         context["first_btn_link"] = instance.glossary.get("first_button_link")
        # elif instance.glossary.get("first_button_link"):
        #     context["first_btn_link"] = instance.glossary.get("first_button_link")

        # if instance.glossary.get("second_button_internallink"):
        #     page = Page.objects.filter(
        #         id=instance.glossary.get("second_button_internallink", {}).get("pk")
        #     ).first()
        #     if page:
        #         context["second_btn_link"] = page.get_absolute_url()
        #     elif instance.glossary.get("second_button_link"):
        #         context["second_btn_link"] = instance.glossary.get("second_button_link")
        # elif instance.glossary.get("second_button_link"):
        #     context["second_btn_link"] = instance.glossary.get("second_button_link")

        return context
@plugin_pool.register_plugin
class PopUpPlugin(CMSPluginBase):
    name = "PopUp"
    module = "Pinogy"
    model = PopupPluginModel
    # form = PopupPluginForm
    render_template = "plugins/popup_plugin/popup_plugin.html"
    # change_form_template = "plugins/popup_plugin/popup_change_form.html"
    alien_child_classes = True
    allow_children = True 
    cache = False

    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        return super().render_change_form(request, context, add, change, form_url, obj)

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        # print(context['instance'])
        return context


@plugin_pool.register_plugin
class HeaderPlugin(CascadePluginBase):
    name = "Header"
    module = "Pinogy"
    model = HeaderPluginModel
    form = HeaderPluginForm
    render_template = "plugins/header/header_plugin.html"
    change_form_template = "plugins/header/header_change_form.html"
    cache = False

    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        if obj is not None:
            pagesInMenu = list(Page.objects.filter(publisher_is_draft=True,title_set__publisher_state = 0, in_navigation = True).values_list('id',flat=True))
            pagesInMenu = [ f'{i}' for i in pagesInMenu]
            custompages = obj.glossary.get('custom_menus' or [])
            result = [item for item in custompages if '#' in item] + pagesInMenu
            context["available_links"] = result

        context["logos"] = ThemeImages.objects.filter(image_type="logo")
        pages = Page.objects.filter(publisher_is_draft=True,title_set__publisher_state = 0).order_by('node__path')
        draft_pages = Page.objects.filter(publisher_is_draft=True).order_by('node__path') # this data is to show pages in internal dropdown
        
        draft_page = [] 
        for draft in draft_pages:
            title = draft.get_menu_title()

            url = draft.title_set.all().first().redirect or draft.get_absolute_url()
            if title != '' and title != None:
                draft_page.append((title,url,draft.id))
        context['draft_pages'] = draft_page # this is the drop down data of internal link
        context['page_tree'] = self.get_page_tree(pages)

        # TO SHOW THE MOBILE NUMBER AND SOCIAL ICON ON PLUGIN PREVIEW SECTION
        client = PWAPI()
        store_id = ( request.session.get('store_location_id') 
            if request.session.get('store_location_id')
            else request.COOKIES.get('store_location_id')
        )
        selected_store = utils.get_selected_store(client=client, store_id=store_id)
        context['store_number'] = selected_store['marketing_phone']
        context['social_links'] = selected_store['social_links']
        context['receipt_name'] = selected_store['receipt_name']
        context['zipcode'] = selected_store['entity']['postal_code']

        ''' sending data to show the quick links in plugin '''
        external_links = list(External_links.objects.filter(parentId__isnull = False, draftId = '0').order_by('id').values())
        context['external_links'] = external_links

        return super().render_change_form(request, context, add, change, form_url, obj)
    
    def get_page_tree(self, pages):
        page_dict = {page.node_id: page for page in pages}
        for page in pages:
            page.children = []

        root_pages = []
        for page in pages:
            parent_id = page.node.parent_id
            if parent_id:
                parent = page_dict.get(parent_id)
                if parent:
                    parent.children.append(page)
            else:
                root_pages.append(page)
        
        return root_pages
    
    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        client = PWAPI()
        context["instance"] = instance
        
        request = context["request"]
        store_id = ( request.session.get('store_location_id') 
            if request.session.get('store_location_id')
            else request.COOKIES.get('store_location_id')
        )
        selected_store = utils.get_selected_store(client=client, store_id=store_id)

        integrations = client.get_website_data()
        if 'ecommerce_enabled' in integrations:
            context['ecommerce_enabled']=integrations['ecommerce_enabled']

        context["selected_store"] = selected_store
        stores_data = utils.get_stores_data(client=client)
        ''' 
        manipulate store address and send to templates
        '''
        for i in range(len(stores_data)):
            stores_data[i]['store_address'] = stores_data[i]['entity']['address_1'] + " " + stores_data[i]['entity']['city']  + " " +  stores_data[i]['entity']['iso_code']  + " " +  stores_data[i]['entity']['postal_code']
            
            current_day = datetime.now().strftime("%A")
            open_hrs = current_day in stores_data[i]['open_hours'] 
            
            try:
                x = utils.convert_to_12hr_format([stores_data[i]['open_hours'][current_day][1]])[0]
            except:
                pass
            stores_data[i]['store_close_time'] = 'Open until '+ x if open_hrs and type(stores_data[i]['open_hours'][current_day]) == type([]) else "Closed"
            
            new_obj = ProductClient()
            delivery_types_obj = new_obj.get_global_delivery_types(customer_zip = stores_data[i]['entity']['postal_code'])
            if delivery_types_obj:
                delivery_types = []
                for j in delivery_types_obj['objects']:
                    delivery_types.append(j['name'])
                stores_data[i]['delivery_types'] = delivery_types
        context["stores_data"] = stores_data
        context['collection_form'] = CollectionForm()

        ''' GET THE STATE AND COUNTRY NAMES FROM APIS '''
        client = CustomerClient()
        countries = get_country_list(client, store_id)
        regions = get_country_regions(client, countries[0]['id'])['objects']
        context['regions'] = regions
        context['countries'] = countries
        
        if request.COOKIES.get('user'):
            context['active_user'] = json.loads(request.COOKIES.get('user')) or ""
        
        # Shop related URLs
        ''' check weather the Pinogy_shop app hook is available or not'''

        if Page.objects.filter(application_namespace = 'pinogy_shop').exists() and request.COOKIES.get('user'):
            pinogy_shop = True
        else:
            pinogy_shop = False
        context['pinogy_shop'] = pinogy_shop

        ''' DATA TO SHOW ADDED QUICKLINKS IN HEADER'''
        page_tree = list(External_links.objects.filter(parentId__isnull = False).values())

        ''' MANIPULATE THE DATA TO SHOW ADD THE INTERNAL LINK URL '''
        for page in page_tree:
            if page['exernal_type'] == 'internal': 
                try:
                    ext_link = Title.objects.get(page_id = int(page['internal_link_id'])).redirect
                    if not ext_link:
                        ext_link = Page.objects.get(id = int(page['internal_link_id'])).get_absolute_url()
                    page['exernal_link_url'] = ext_link
                except:
                    ext_link = ''

        context['quick_links'] = json.dumps(page_tree)
        context['custom_menu'] = json.dumps(instance.glossary.get('custom_menus'))
        try:
            context['shop_card_detail_page_url'] = reverse('pinogy_shop:card_detail_page')
            context['shop_my_account_page_url'] = reverse('pinogy_shop:my_account_page')
            context['shop_product_list_page_url'] = reverse('pinogy_shop:product_list_page')
            context['shop_login_url'] = reverse('pinogy_shop:login')
            context['shop_signup_url'] = reverse('pinogy_shop:signup')
            context['shop_logout_url'] = reverse('pinogy_shop:logout')
            context['shop_checkout_api'] = reverse('pinogy_shop:checkout-api')
            context['shop_update_address'] = reverse('pinogy_shop:update-address')
            context['shop_create_address'] = reverse('pinogy_shop:create-address')
            context['shop_card_url'] = reverse('pinogy_shop:card')
            context['shop_store_list_url'] = reverse('pinogy_shop:store_list')
            context['shop_store_setltlg_url'] = reverse('pinogy_shop:store_setltlg')
            context['shop_delivering_set_url'] = reverse('pinogy_shop:delivering_set', kwargs={'delivering_location_zip': 0})
        except NoReverseMatch:
            context['shop_card_detail_page_url'] = '#'
            context['shop_my_account_page_url'] = '#'
            context['shop_product_list_page_url'] = '#'
            context['shop_login_url'] = '#'
            context['shop_signup_url'] = '#'
            context['shop_logout_url'] = '#'
            context['shop_card_url'] = '#'
            context['shop_store_list_url'] = '#'
            context['shop_store_setltlg_url'] = '#'
            context['shop_store_set_url'] = '#'
            context['shop_delivering_set_url'] = '#'
            context['shop_checkout_api'] = '#'
            context['shop_update_address'] ='#'
            context['shop_create_address'] = '#'

        return context

    def save_model(self, request, obj, form, change):

        with transaction.atomic():
            # THIS BELOW CODE IS TO DELETE THE PAGES 
            deleted_childs = request.POST.get('external_del_childs')
            deleted_childs = json.loads(deleted_childs)
            
            if(deleted_childs != []):
                parent_delete_id = [ data for data in deleted_childs if data.split('#')[0] == 'a']
                if parent_delete_id !=[]:
                    External_links.objects.filter(parentId__in = parent_delete_id).delete()
                for data in  deleted_childs:
                    ids = data.split('#')[0]
                    child_level = data.split('#')[1]
                    if ids != 'a' and Page.objects.filter(id = int(ids)).exists():
                        childid = Page.objects.get(id = ids).node_id
                        page_child_id = str(Page.objects.filter(node_id = childid).exclude(id = int(ids))[0].id)
                        if External_links.objects.filter(parentId = page_child_id, childId = page_child_id+"#"+child_level).exists():
                            External_links.objects.get(parentId = page_child_id, childId = page_child_id+"#"+child_level).delete()
                External_links.objects.filter(childId__in = deleted_childs).delete()

            # TO SAVE EXTERNAL LINKS
            external_links = request.POST.getlist('external_links', [])
            all_child_ids = []
            for indexes in external_links:

                ids_data = indexes.split('#') or None

                parent_id = ids_data[0]
                ''' get the id of the page that will created after pulished '''
                if parent_id != 'a' and Page.objects.filter(id = int(parent_id)).exists():
                    node_id = Page.objects.get(id = int(parent_id)).node_id
                    page_node_id = Page.objects.filter(node_id = node_id).exclude(id = parent_id)[0].id
                    node_id = str(page_node_id)+"#"+ids_data[1]
                    obj.glossary['custom_menus'].append(node_id)

                all_child_ids = (*all_child_ids, indexes)
                
                ext_link_name = request.POST.get('ext_link_name_'+indexes, '')
                button_target = request.POST.get('button_target_'+indexes)

                # CHECK WEATHER THE LINK TYPE IS INTERNAL OR EXTERNAL
                link_choice_field = request.POST.get('link_choice_field_'+indexes)
                int_link_id = request.POST.get('button_internallink_'+indexes, '')
                ext_link_url = request.POST.get('ext_link_url_'+indexes, '')

                save_data = True
                if link_choice_field == 'internal' and (ext_link_name == '' and int_link_id == ''):
                    save_data = False
                    # ext_link = Title.objects.get(page = int(int_link_id)).redirect
                    # if not ext_link:
                    #     ext_link = Page.objects.get(id = int_link_id).get_absolute_url()
                elif link_choice_field == 'external' and (ext_link_name == '' and ext_link_url == ''):
                    save_data = False
                
                if save_data:
                    if parent_id == 'a' and External_links.objects.filter(parentId = indexes).exists(): 
                        External_links.objects.filter(parentId = indexes).update(exernal_link_name = ext_link_name, exernal_link_url = ext_link_url, exernal_target = button_target, 
                                        exernal_type = link_choice_field, internal_link_id = int_link_id, 
                                        parentId = indexes)
                    elif parent_id == 'a' and not External_links.objects.filter(parentId = indexes).exists(): 
                        External_links.objects.create(ext_page_id = None, exernal_link_name = ext_link_name, exernal_link_url = ext_link_url, exernal_target = button_target, 
                                        exernal_type = link_choice_field, internal_link_id = int_link_id, 
                                        parentId = indexes, childId = None, draftId = '0')

                    # check weather the header child index is in header_quicklink column or not. if yes then 
                    # then update it in title table.
                    elif External_links.objects.filter(childId = indexes).exists():
                        External_links.objects.filter(childId = indexes).update( exernal_link_name = ext_link_name, exernal_link_url = ext_link_url, exernal_target = button_target, 
                                        exernal_type = link_choice_field, internal_link_id = int_link_id, 
                                        )
                        
                        External_links.objects.filter(childId = node_id).update(exernal_link_name = ext_link_name, exernal_link_url = ext_link_url, exernal_target = button_target, 
                                        exernal_type = link_choice_field, internal_link_id = int_link_id, 
                                        )
                    else:
                        External_links.objects.create(ext_page_id = parent_id, exernal_link_name = ext_link_name, exernal_link_url = ext_link_url, exernal_target = button_target, 
                                        exernal_type = link_choice_field, internal_link_id = int_link_id, draftId = '0',
                                        parentId = parent_id, childId = indexes)
                        External_links.objects.create(ext_page_id = page_node_id, exernal_link_name = ext_link_name, exernal_link_url = ext_link_url, exernal_target = button_target, 
                                        exernal_type = link_choice_field, internal_link_id = int_link_id, draftId = '1',
                                        parentId = page_node_id, childId = node_id)
            
            obj.glossary['custom_menus'].extend(all_child_ids)
            obj.save()
            ''' save the checked data and add it in navigation or remove from navigation'''
            checked_link = request.POST.getlist("custom_menus")
            if checked_link:
                published_page_ids = []
                for link in checked_link:
                    node_id = Page.objects.get(id = int(link)).node_id 
                    page_node_id = Page.objects.filter(node_id = node_id).exclude(id = int(link))[0].id
                    published_page_ids.append(str(page_node_id))
                published_page_ids.extend(checked_link)
                publ_page = Page.objects.filter(id__in = published_page_ids)
                publ_page.update(in_navigation = True)
                obj.glossary['custom_menus'].extend(checked_link) 
                obj.save()

                ''' try to find which checkbox is not selected '''

                links_excluded_data = Page.objects.filter(publisher_is_draft=True,in_navigation = True).values_list('id',flat=True)
                res = [ d for d in links_excluded_data if str(d) not in checked_link]
                if res:
                    unpubpageids = []
                    for d in res:
                        node_id = Page.objects.get(id = d).node_id 
                        page_node_id = Page.objects.filter(node_id = node_id).exclude(id = d)[0].id
                        unpubpageids.append(page_node_id)
                     
                    unpubpageids.extend(res)
                    pageUnpublished = Page.objects.filter(id__in = unpubpageids)
                    pageUnpublished.update(in_navigation = False)
                cache.clear()
                
        super().save_model(request, obj, form, change)

@plugin_pool.register_plugin
class FooterPlugin(CascadePluginBase):
    name = "Footer"
    module = "Pinogy"
    model = FooterPluginModel
    form = FooterPluginForm
    render_template = "plugins/footer/footer_plugin.html"
    change_form_template = "plugins/footer/footer_change_form.html"
    cache = False

    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        context["logos"] = ThemeImages.objects.filter(image_type="logo")
        return super().render_change_form(request, context, add, change, form_url, obj)
    
    def handle_hours(self, week_hours):
        for day in week_hours.keys():
            week_hours[day] = utils.convert_to_12hr_format(week_hours[day])
        
        return week_hours

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        client = PWAPI()

        WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        context["instance"] = instance
        request = context["request"]
        
        dynamic_store_id = request.session.get('store_location_id') or request.COOKIES.get('store_location_id')

        # First Location Data
        if instance.glossary.get("first_location"):
            store_id = instance.glossary.get("first_location")
        else:
            store_id = dynamic_store_id
        selected_store = utils.get_selected_store(client=client, store_id=store_id)
        context["selected_store"] = selected_store
        
        # second Location Data
        second_store = {}
        if instance.glossary.get("second_location"):
            store_id = instance.glossary.get("second_location")
            second_store = utils.get_selected_store(client=client, store_id=store_id)
            context["second_selected_store"] = second_store

        # Add store data based on session or cookies
        dynamic_store_data = None
        if not dynamic_store_id:
            dynamic_store_id = store_id

        if dynamic_store_id == store_id:
            dynamic_store_data = selected_store
        elif dynamic_store_id ==  instance.glossary.get("second_location"):
            dynamic_store_data = second_store
        else:
            dynamic_store_data = utils.get_selected_store(client=client, store_id=dynamic_store_id)

        context['dynamic_store_data'] = dynamic_store_data

        # Sorting openig hours as per week days
        if selected_store.get('open_hours'):
            opening_days = self.handle_hours(selected_store.get('open_hours'))
            context['open_hours'] = sorted(opening_days.items(), key= lambda pair:WEEKDAYS.index(pair[0]))

        # quicklinks data
        quicklink_inst = instance.glossary.get("quick_links")
        # fix 500 02/04
        if quicklink_inst:
            query_obj=Page.objects.filter(publisher_is_draft=True,title_set__publisher_state = 0, id__in = quicklink_inst).order_by('node__path')
            quick_linked = [{'name' : d.get_menu_title(),'url' : d.get_absolute_url()} for d in query_obj]
            try:
                jsonData = json.loads(instance.external_quick_links).items()
            except:
                jsonData = {}
            c = []
            for key,value in jsonData:
                if value['check'] == 'checked':
                    try: 
                        value['link_target']
                    except:
                        value['link_target'] = '_self'
                    c.append({'name' : value['name'], 'url' : value['url'], 'target' : value['link_target']})
            # c = [ {'name' : value['name'], 'url' : value['url'], 'target' : value['link_target'] } for key,value in jsonData if value['check'] == 'checked']
            context['quick_linked'] = quick_linked + c
        return context


@plugin_pool.register_plugin
class InfoBlockFirstPlugin(CascadePluginBase):
    name = "Info Block Plugin"
    module = "Pinogy"
    model = InfoBlockFirstPluginModel
    form = InfoBlockFirstPluginForm
    render_template = "plugins/infoblock_first/infoblockfirst_plugin.html"
    change_form_template = "plugins/infoblock_first/infoblockfirst_change_form.html"
    cache = False

    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        return super().render_change_form(request, context, add, change, form_url, obj)
    
    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        if instance.glossary.get("button_internallink"):
            page = Page.objects.filter(
                id=instance.glossary.get("button_internallink", {}).get("pk")
            ).first()
            if page:
                context["btn_link"] = page.get_absolute_url()
            elif instance.glossary.get("button_link"):
                context["btn_link"] = instance.glossary.get("button_link")
        elif instance.glossary.get("button_link"):
            context["btn_link"] = instance.glossary.get("button_link")
        context["layout_type1"] = ['LAYOUT1','LAYOUT2','LAYOUT3','LAYOUT4']
        context["layout_type2"] = ['LAYOUT5','LAYOUT7']
        context["layout_type3"] = ['LAYOUT8','LAYOUT9', 'LAYOUT10', 'LAYOUT11']
        context["video_layout_type"] = ['LAYOUT13','LAYOUT14']
        context['franchise_form'] = CollectionForm

        return context
    
    def get_render_template(self, context, instance, placeholder):
        # if instance.glossary.get("layout") == "LAYOUT5" or instance.glossary.get("layout") == "LAYOUT7":
            
        #     return "plugins/infoblock_first/info_block_full_image.html"

        if instance.glossary.get("media_type") == 'Image' and instance.glossary.get("layout") == "LAYOUT6" and instance.glossary.get("quantity_of_image") == 'QTY1':
            return "plugins/infoblock_first/info_block_with_form.html"

        return "plugins/infoblock_first/infoblockfirst_plugin.html"


@plugin_pool.register_plugin
class InfoBlockSecondPlugin(CascadePluginBase):
    name = "Info Block Plugin Second"
    module = "Pinogy"
    model = InfoBlockSecondPluginModel
    form = InfoBlockSecondPluginForm
    render_template = "plugins/infoblock_second/infoblocksecond_plugin.html"
    change_form_template = "plugins/infoblock_second/infoblocksecond_change_form.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        if instance.glossary.get("button_internallink"):
            page = Page.objects.filter(
                id=instance.glossary.get("button_internallink", {}).get("pk")
            ).first()
            if page:
                context["btn_link"] = page.get_absolute_url()
            elif instance.glossary.get("button_link"):
                context["btn_link"] = instance.glossary.get("button_link")
        elif instance.glossary.get("button_link"):
            context["btn_link"] = instance.glossary.get("button_link")

        return context


@plugin_pool.register_plugin
class SliderPlugin(CascadePluginBase):
    name = "Slider Plugin"
    module = "Pinogy"
    model = SliderPluginModel
    form = SliderPluginForm
    render_template = "plugins/slider/slider_plugin.html"
    change_form_template = "plugins/slider/slider_change_form.html"
    allow_children = True
    cache = False


@plugin_pool.register_plugin
class StaticInfoBlockPlugin(WithInlineElementsMixin, CascadePluginBase):
    
    name = "Static Info Block"
    module = "Pinogy"
    form = StaticInfoBlockPluginForm
    inlines = [StaticInfoItemInline]
    render_template = "plugins/static_info_block/static_info_block_plugin.html"
    cache = True

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        
        # Adding image obj for url
        static_items = instance.inline_elements.all()
        for static_item in static_items:

            # Get filer image obj by pk and add into glossary field image dict
            try:
                Model = apps.get_model(static_item.glossary['image_file']['model'])
                image_obj = Model.objects.get(pk=static_item.glossary['image_file']['pk'])
                if static_item.glossary.get("button_internallink"):
                    page = Page.objects.filter(
                    id=static_item.glossary.get("button_internallink", {}).get("pk")
                    ).first()
                    if page:
                        static_item.glossary['btn_link']= page.get_absolute_url()
                    elif static_item.glossary.get("url"):
                        static_item.glossary['btn_link'] = static_item.glossary.get("url")
                else:
                    static_item.glossary['btn_link']=static_item.glossary['url']
            except Exception as e:
                print(e)
                image_obj = None

            static_item.glossary['image_file']['image'] = image_obj
        
        context['items'] = static_items

        if instance.glossary.get("main_button_internallink"):
            page = Page.objects.filter(
                id=instance.glossary.get("main_button_internallink", {}).get("pk")
            ).first()
            if page:
                context["main_btn_link"] = page.get_absolute_url()
            elif instance.glossary.get("main_button_link"):
                context["main_btn_link"] = instance.glossary.get("main_button_link")
        elif instance.glossary.get("main_button_link"):
            context["main_btn_link"] = instance.glossary.get("main_button_link")
        
        return context

@plugin_pool.register_plugin
class ContactUsPlugin(CascadePluginBase):
    name = "ContactUs Plugin"
    module = "Pinogy"
    form = ContactUsPluginForm
    render_template = "plugins/contact_us/contact_us_plugin.html"
    change_form_template = "custom_design/admin/change_form.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        client = PWAPI()
        request = context["request"]
        context["host"] = request.get_host()
        context['collection_form'] = CollectionForm()
        shopwindow_location_ids = utils.get_shopwindow_location_ids()
        api_stores = utils.get_stores_data(client=client)
        selected_stores = instance.glossary.get("location_filter", [])
        stores = []
        # checking if store has shopwindow enabled or not
        for store in api_stores:
            if store['id'] in shopwindow_location_ids:
                store['shopwindow_enable'] = True
            else:
                store['shopwindow_enable'] = False
                
        if selected_stores:
            stores.extend(store for store in api_stores if str(store['id']) in selected_stores)
        else:
            stores = api_stores
        
        # getting all the stores latitude,longitude and address to show in map
        gmap_store_data = []

        for store in api_stores:
            if str(store['id']) in selected_stores or len(selected_stores) == 0:
                current_store = {
                    'lat': float(store.get('latitude') if store.get('latitude') else 0),
                    'lng': float(store.get('longitude') if store.get('longitude') else 0),
                    'address': (
                        f"{store['entity']['address_1']}, "
                        f"{store['entity']['city']}, "
                        f"{store['entity']['region_fullname']}, "
                        f"{store['entity']['postal_code']}"
                    ),
                    'receipt_name': store.get('receipt_name')
                }
                gmap_store_data.append(current_store)



        context["selected_store"] = stores
        context["gmap_store_data"] = gmap_store_data
        
        return context

@plugin_pool.register_plugin
class TestimonialsPlugin(CascadePluginBase):
    name="Featured Testimonials"
    module="Pinogy"
    render_template = "plugins/testimonial_plugin/testimonia_plugin.html"
    cache = False
    
    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        items = Testimonial.objects.filter(is_published=True, is_featured=True)
        context["instance"] = items[:5]
        
        return context

@plugin_pool.register_plugin
class SubscribePlugin(CascadePluginBase):
    name = "Newsletter"
    module = "Pinogy"
    model = SubscribePluginModel
    form = SubscribeUsPluginForm
    render_template = "plugins/subscribe_us/subscribe_us_plugin.html"
    change_form_template = "plugins/subscribe_us/subscribe_us_change_form.html"
    cache = False

    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
        ):
        context['subscribe_form'] = SubscribeUsForm()
        return super().render_change_form(request, context, add, change, form_url, obj)
    
    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        client = PWAPI()
        request = context["request"]

        # getting current store_id
        store_data = get_stores_data(client=client)
        default_store_id = None
        if len(store_data) > 0:
            default_store_id = store_data[0].get('id',None)

        store_id = request.session.get('store_location_id') or \
            request.COOKIES.get('store_location_id') or default_store_id
        
        context['location_id'] = store_id
        
        # Get Bg Image Url
        # if instance.glossary.get("bg_image"):
        #     Model = apps.get_model(instance.glossary['bg_image']['model'])
        #     try:
        #         instance.glossary['bg_image']['url'] = Model.objects.get(pk=instance.glossary['bg_image']['pk']).url
        #     except Model.DoesNotExist:
        #         instance.glossary.pop('bg_image', '')
        
        # # Get Side Image Url
        # if instance.glossary.get("side_image"):
        #     Model = apps.get_model(instance.glossary['side_image']['model'])
        #     try:
        #         instance.glossary['side_image']['url'] = Model.objects.get(pk=instance.glossary['side_image']['pk']).url
        #     except Model.DoesNotExist:
        #         instance.glossary.pop('side_image', '')
        context['marketing_list'] = instance.glossary.get('marketing_list')
        context['marketing_btn_style'] = instance.glossary.get('marketing_button_color')
        context['marketing_button_text'] = instance.glossary.get('marketing_button_text')
        context['subscribe_form'] = SubscribeUsForm()

        return context

@plugin_pool.register_plugin
class UnSubscribePlugin(CascadePluginBase):
    name =  "UnSubscribe Plugin"
    module = "Pinogy"
    model = UnSubscribePluginModel
    form = UnSubscribeUsPluginForm
    render_template = "plugins/unsubscribe/unsubscribe.html"
    change_form_template = "plugins/unsubscribe/unsubscribe_change_form.html"
    cache = False

    def get_token_details(self, token):
        try:
            client = PWAPI()
            token_data = client.verify_unsubscribe_token(token)
            if token_data:
                return True
            else:
                return False
        except Exception as e:
            return False


    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        request = context['request']
        token = request.GET.get('token',None)
        is_token_verified = self.get_token_details(token)
        context['is_token_verified'] = is_token_verified
        context['token'] = token
        return context
     
    
@plugin_pool.register_plugin
class GalleryPlugin(WithInlineElementsMixin, CascadePluginBase):
    name = "Gallery"
    module = "Pinogy"
    form = GalleryPluginForm
    inlines = [GalleryItemInline]
    render_template = "plugins/gallery/gallery_plugin.html"
    change_form_template = "custom_design/admin/change_form.html"
    cache = True

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        
        # Adding image obj for url
        gallery_images = instance.inline_elements.all().order_by('id')
        for gallery_image in gallery_images:

            # Get filer image obj by pk and add into glossary field image dict
            try:
                Model = apps.get_model(gallery_image.glossary['image_file']['model'])
                image_obj = Model.objects.get(pk=gallery_image.glossary['image_file']['pk'])
            except Exception as e:
                print(e)
                image_obj = None

            gallery_image.glossary['image_file']['image'] = image_obj

            gallery_image.double_image_width = (
                gallery_image.glossary.get("image_size", GalleryItemForm.SQUARE_IMAGE) == GalleryItemForm.DOUBLE_IMAGE
            )

            context['images'] = gallery_images
        
        return context


@plugin_pool.register_plugin
class ServicesBlockPlugin(WithInlineElementsMixin, CascadePluginBase):
    name = "Services Block Plugin"
    module = "Pinogy"
    form = ServicesBlockPluginForm
    inlines = [ServiceItemInline]
    render_template = "plugins/services_block/service_block.html"
    change_form_template = "custom_design/admin/change_form.html"
    cache = False
    
    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        
        # Adding image obj for url
        services = instance.inline_elements.all()
        for service in services:

            # Get filer image obj by pk and add into glossary field image dict
            try:
                Model = apps.get_model(service.glossary['image_file']['model'])
                image_obj = Model.objects.get(pk=service.glossary['image_file']['pk'])
                
            except Exception as e:
                print(e)
                image_obj = None

            service.glossary['image'] = image_obj
        
        context['services'] = services
        
        return context
    


@plugin_pool.register_plugin
class ContactUsInfoPlugin(CascadePluginBase):
    name = "ContactUs Info Plugin"
    module = "Pinogy"
    model = ContactUsInfoPluginModel
    form = ContactUsInfoPluginForm
    render_template = "plugins/contactUsInfo_plugin/contactUsInfo_plugin.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        client = PWAPI()
        # Get Bg Image Url
        if instance.glossary.get("bg_image"):
            Model = apps.get_model(instance.glossary['bg_image']['model'])
            try:
                instance.glossary['bg_image']['url'] = Model.objects.get(pk=instance.glossary['bg_image']['pk']).url
            except Model.DoesNotExist:
                instance.glossary.pop('bg_image', '')
        
        # Get Side Image Url
        if instance.glossary.get("side_image"):
            Model = apps.get_model(instance.glossary['side_image']['model'])
            try:
                instance.glossary['side_image']['url'] = Model.objects.get(pk=instance.glossary['side_image']['pk']).url
                if instance.glossary.get("button_internallink"):
                    page = Page.objects.filter(
                    id=instance.glossary.get("button_internallink", {}).get("pk")
                    ).first()
                    if page:
                        instance.glossary['btn_link']= page.get_absolute_url()
                    elif instance.glossary.get("url"):
                        instance.glossary['btn_link'] = instance.glossary.get("url")
                else:
                    if instance.glossary.get('url'):
                        instance.glossary['btn_link']=instance.glossary['url']

                request = context["request"]
                dynamic_store_id = request.session.get('store_location_id') or request.COOKIES.get('store_location_id')
                if instance.glossary.get("first_location"):
                    store_id = instance.glossary.get("first_location")
                else:
                    store_id = dynamic_store_id
                selected_store = utils.get_selected_store(client=client, store_id=store_id)
                context["store"] = selected_store
                context['subscribe_form'] = SubscribeUsForm()
            except Model.DoesNotExist:
                instance.glossary.pop('side_image', '')
        return context

@plugin_pool.register_plugin
class CardCarouselPlugin(CMSPluginBase):
    module = 'Pinogy'
    model = CardCarouselModel
    name = 'Static Slider'
    allow_children = True
    render_template = 'common_plugins/plugins/card_carousel.html'

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


@plugin_pool.register_plugin
class FAQBlockPlugin(WithInlineElementsMixin, CascadePluginBase):
    
    name = "FAQ Block"
    module = "Pinogy"
    form = FAQBlockPluginForm
    inlines = [FAQTabInline]
    render_template = "plugins/faq_block/faq_block_plugin.html"
    allow_children = True
    child_classes = ['FAQAccordionPlugin']
    cache = True

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        
        faq_tabs = instance.inline_elements.all()
        context['tabs'] = faq_tabs
        return context
    

@plugin_pool.register_plugin
class FAQAccordionPlugin(WithInlineElementsMixin, CascadePluginBase):
    
    name = "FAQ Accordion"
    module = "Pinogy"
    form = FAQAccordionPluginForm
    inlines = [FAQItemInline]
    require_parent = True
    parent_classes = ['FAQBlockPlugin']
    render_template = "plugins/faq_block/faq_accordion_plugin.html"
    cache = True

    def render(self, context, instance, placeholder):
        context = super(FAQAccordionPlugin, self).render(context, instance, placeholder)
        
        faq_items = instance.inline_elements.all()
        context['items'] = faq_items

        return context
    
@plugin_pool.register_plugin
class LocationContactNumberPlugin(CascadePluginBase):
    name = "Location Contact Number"
    module = "Pinogy"
    form = LocationContactNumberPluginForm
    render_template = "common_plugins/plugins/location_contact_number.html"
    change_form_template = "custom_design/admin/change_form.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        client = PWAPI()

        request = context["request"]
        
        store_id = request.session.get('store_location_id') or \
            request.COOKIES.get('store_location_id') or \
            instance.glossary.get("location")
        selected_store = utils.get_selected_store(client=client, store_id=store_id)

        context.update({
            "font_color": instance.glossary.get("text_color", "#000"),
            "contact_number": selected_store.get("store_contact"),
        })

        return context

@plugin_pool.register_plugin
class LocationSocialPlugin(CascadePluginBase):
    name = "Location Social Icons"
    module = "Pinogy"
    form = LocationSocialPluginForm
    render_template = "common_plugins/plugins/location_social.html"
    change_form_template = "custom_design/admin/change_form.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        client = PWAPI()

        request = context["request"]
        
        store_id = request.session.get('store_location_id') or \
            request.COOKIES.get('store_location_id') or \
            instance.glossary.get("location")
        selected_store = utils.get_selected_store(client=client, store_id=store_id)


        context.update({
            "font_color": instance.glossary.get("text_color", "#000"),
            "social_links": {key.lower(): value for key, value in (selected_store.get('social_links') or {}).items()},
        })

        return context
    
@plugin_pool.register_plugin
class InstagramPlugin(CMSPluginBase):
    name = "Instagram"
    module = "Pinogy"
    model = InstagramFeedPluginModel
    render_template = "plugins/instagram/instagram_feed.html"
    cache = False

    def render(self, context, instance, placeholder):
        """
        Render method for displaying Instagram feeds.
        
        Args:
        context (dict): Rendering context.
        instance (InstagramFeedPluginModel): Plugin instance.
        placeholder (str): Placeholder for the plugin.
        
        Returns:
        dict: Updated rendering context.
        """
        context = super().render(context, instance, placeholder)
        
        # Retrieve access token and plugin ID from the plugin instance
        access_token = instance.access_token
        plugin_id = instance.cmsplugin_ptr_id
        
        # Fetch Instagram data using utility function
        context['posts'] = utils.instagram_data(access_token, plugin_id)
        
        return context
    
@plugin_pool.register_plugin
class ShowHidePlugin(CascadePluginBase):
    name = "Show/Hide Plugin"
    module = "Pinogy"
    form = ShowHidePluginForm
    allow_children = True
    render_template = "plugins/show_hide/show_hide_plugin.html"
    change_form_template = "plugins/show_hide/show_hide_change_form.html"
    cache = False


    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        return super().render_change_form(request, context, add, change, form_url, obj)
    
    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        client = PWAPI()
        request = context["request"]

        # getting current store_id
        store_data = get_stores_data(client=client)
        default_store_id = None
        if len(store_data) > 0:
            default_store_id = store_data[0].get('id',None)

        store_id = request.session.get('store_location_id') or \
            request.COOKIES.get('store_location_id') or default_store_id
        
        # checking if current date is in selected date range or not 
        # if current date is in range set current_date_in_range to True else False
        # same for store location
        
        context['current_store_in_list'] = False
        if str(store_id) in instance.glossary.get('sh_store_locations',[]):
            context['current_store_in_list'] = True

        context['current_date_in_range'] = False
        if instance.glossary.get('sh_date_range'):
            current_date = date.today()
            date_split = instance.glossary.get('sh_date_range',"").split(" ")
            start_date = datetime.strptime(date_split[0], "%Y-%m-%d").date()
            if len(date_split) == 2:
                end_date  = datetime.strptime(date_split[1], "%Y-%m-%d").date()
            else:
                end_date = start_date

            if  current_date >= start_date and current_date <= end_date:
                context['current_date_in_range'] = True
        
        context['filter_type'] = instance.glossary.get('sh_filter_type',False) 

        if instance.glossary.get('sh_date_choice'):
                context['sh_date_choice'] = instance.glossary.get('sh_date_choice')[0]
        
        if instance.glossary.get('sh_location_choice'):
                context['sh_location_choice'] = instance.glossary.get('sh_location_choice')[0]
        

        return context

@plugin_pool.register_plugin
class TabsPlugin(CMSPluginBase):
    name =  "Tabs"
    module = "Testing"
    model = TabsCompoPluginModel
    render_template = "plugins/tabs/tabs.html"
    allow_children = True  
    child_classes = ["TabItemPlugin"]  # Restrict child plugins to TabItem only

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['tabs'] = instance
        return context

@plugin_pool.register_plugin
class TabItemPlugin(CMSPluginBase):
    name =  "Tab Item"
    module = "Testing"
    model = TabItemCompoPluginModel
    render_template = "plugins/tabs/tab_item.html"
    parent_classes = ["TabsPlugin"]  # Restrict parent to only be the Tabs plugin
    allow_children = True  

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['tab'] = instance.get_children()  # Pass the tab instance to the template
        return context
    
