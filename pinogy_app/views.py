import os

from django.http import JsonResponse, HttpResponse, Http404
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.sites.models import Site
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.translation import activate, deactivate
from django.contrib.sites.shortcuts import get_current_site
from cms.models import Title
from cms.apphook_pool import apphook_pool
from cms.sitemaps import CMSSitemap
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import render
from .models import SiteMapModel
from pos_api.pos_client import PWAPI
import json
xml_path = os.getcwd()

def health_check(request):
    """
    return website version, host etc
    """
    return JsonResponse({
        'API_HOST': settings.PINOGY_API_HOST, 
        'BASE_TYPE': settings.BASE_TYPE,
        'CLIENT_ID': settings.CLIENT_ID,
        'DEPLOYED_VERSION': getVersion(),
        'HOSTNAME': settings.HOST_NAME, 
        'INTEGRATION_ID': settings.INTEGRATION_ID,
        'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY
    })

def getVersion():
    xml_path = os.getcwd()
    file_path = f'{xml_path}/IMAGE_BUILD.txt'
    try:
        with open(file_path) as f:
            contents = f.readlines()
        if len(contents)>0:
            return contents[0].strip()
        else:
            return ''
    except Exception as e:
       return ''

def redirect_reset(request):
    code = request.GET.get('code')
    if not code or not apphook_pool.get_apphook('PinogyShopApphook'):
        raise Http404   
    return redirect(reverse('pinogy_shop:reset_approve', kwargs=dict(code=code)))

def get_sitemap_view(request):
    try:
        latest_entry = SiteMapModel.objects.latest('id')
        document_url = latest_entry.document.url if latest_entry.document else None
        file_path = os.path.join(settings.MEDIA_ROOT, document_url.lstrip('/')).replace('/media/', '/')
        read_file = open(file_path).read()
        return HttpResponse(read_file, content_type='text/xml')
    except Exception as e:
        return sitemap(request=request, sitemaps={'cmspages': CMSSitemap})


def readFileview(request,file_name):
    current_site = Site.objects.get_current()
    if current_site:
        file_path = f'{xml_path}/static_collected/{file_name}'
        try:
            with open(file_path) as f:
                contents = f.readlines()
            return HttpResponse(contents, content_type='text/plain')
        except Exception as e:
            return sitemap(request=request, sitemaps={'cmspages': ''})


class SitemapDataAPI(View):
    """
    API endpoint that returns all page-related data necessary to create a sitemap file,
    separating static pages and Apphook pages, with domain and protocol separated.
    Requires a valid secret key provided in the 'X-Secret-Key' header.
    """
    template_name = 'pinogy_app/plugins/un.html'
    success_url_name = 'pinogy_shop:checkout'
    def get(self, request, *args, **kwargs):
        # Validate the secret key
        secret_key = request.headers.get('X-Secret-Key')
        if secret_key != settings.PINOGY_SECRET_KEY:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        site = get_current_site(request)
        protocol = request.scheme
        languages = settings.LANGUAGES

        # Get all titles for the current site that are publicly accessible
        cms_titles = Title.objects.public().filter(
            language__in=[lang[0] for lang in languages],
            page__login_required=False,
            page__node__site=site,
        ).order_by('page__node__path')

        # Instantiate CMSSitemap to reuse its lastmod and location methods
        cms_sitemap = CMSSitemap()

        static_pages_data = []
        apphook_pages_data = []

        for title in cms_titles:
            page = title.page

            # Use the CMSSitemap's lastmod method to determine the last modification date
            lastmod = cms_sitemap.lastmod(title)

            # Check if the page has an Apphook
            apphook = page.application_urls

            # Activate the correct language context for generating the URL path
            activate(title.language)
            path = cms_sitemap.location(title)
            deactivate()

            if apphook:
                # This is an Apphook page
                apphook_data = {
                    "path": path,
                    "lastmod": lastmod.strftime('%Y-%m-%d') if lastmod else None,
                    "changefreq": "monthly",  # Adjust according to your needs
                    "priority": 0.5,  # Adjust according to your needs
                    "apphook_name": apphook
                }

                if apphook_data not in apphook_pages_data:
                    apphook_pages_data.append(apphook_data)
            else:
                # This is a static page
                static_page_data = {
                    "path": path,
                    "lastmod": lastmod.strftime('%Y-%m-%d') if lastmod else None,
                    "changefreq": "monthly",  # Adjust according to your needs
                    "priority": 0.5  # Adjust according to your needs
                }

                static_pages_data.append(static_page_data)

        # Return the combined data as JSON
        return JsonResponse({
            "protocol": protocol,
            "domain": site.domain,
            "static_pages": static_pages_data,
            "apphooks": apphook_pages_data
        }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class SiteMapWebhook(View):
    """
    Handle file uploads via a POST request to the /webhook/sitemap/ endpoint.

    This view accepts an XML file and saves it using the SiteMapModel.
    The request must include a valid 'X-Secret-Key' header for authentication.
    """
    def post(self, request, *args, **kwargs):
        secret_key = request.headers.get('X-Secret-Key')
        if secret_key != settings.PINOGY_SECRET_KEY:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        xml_file = request.FILES['file']
        if not xml_file.name.endswith('.xml'):
            return JsonResponse({'error': 'File is not an XML file'}, status=400)
        
        # Create a new instance of SiteMapModel and save the uploaded file
        sitemap_instance = SiteMapModel(document=xml_file)
        sitemap_instance.save()
        
        return JsonResponse({'message': 'File uploaded successfully', 'file_id': sitemap_instance.pk}, status=201)
 
class UnSubscribePlugin(View):
    template_name = 'plugins/unsubscribe/unsubscribe.html'
    def get(self, request, *args, **kwargs):
        client = PWAPI()
        mk_list=client.Marketing_emails()
        data=mk_list['objects']
        marketing_email=''
        if(len(data)>0):
            marketing_email=next((item['name'] for item in mk_list['objects'] if item['id'] == -3), None)
        try:
            token_value = request.GET.get('token')
            token_data = client.verify_unsubscribe_token(token_value)
            obj={
                'token':token_data,
                'marketing_email':marketing_email,
                'sucess':True
            }
            return render(request, self.template_name, context=obj)
        except Exception as e:
            obj={
                'token':{},
                'marketing_email':marketing_email,
                'validation_error':True
            }
            # Create obj if token is not avalable or not in correct format 
            return render(request, self.template_name, context=obj)
        
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            client = PWAPI()
            user_token = client.unsubscribe_marketing_lists(data)
            return JsonResponse({'success': True,'data':user_token})
        except Exception as e:
            obj={
                'token':{},
                'marketing_email':'marketing_email',
                'validation_error':True
            }
            return JsonResponse({'error': 'Unauthorized'}, status=401)
      
            
class Subscribe(View):
    template_name = 'plugins/unsubscribe/subscribe.html' 
    def get(self, request, *args, **kwargs):
        client = PWAPI()
        try:
            token_value = request.GET.get('token')
            data={
                'status': 'Subscribed',
                'token': token_value
            }
            token_data = client.subscribe_marketing_lists(data)

            return render(request, self.template_name, context=token_data)
        except Exception as e:
            return render(request, self.template_name, context={})
        