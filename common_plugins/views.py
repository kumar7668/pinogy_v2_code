import json
import datetime
import re
import pytz

from django.utils.dateparse import parse_datetime
from django.shortcuts import render  # noqa
from django.views.generic import FormView, View
from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from uszipcode import SearchEngine
from .models import HeaderPluginModel
from pos_api.pos_client import PWAPI
from common_plugins.forms import CollectionForm, SchedulePlaydate, SubscribeUsForm, AvailablePuppyCollectionForm,CustomerVerificationForm,OtpVerificationForm
from custom_design.models import ThemeImages
from django.conf import settings
from django.core.cache import cache
import requests
from pinogy_shop.pos_api.customer import EntityClient
class CollectionFormMixin(FormView):

    def form_valid(self, form):
        context = self.get_context_data()
        context['form'] = self.form_class
        client = PWAPI()
        
        form_data = form.cleaned_data

        # Get user's IP address from the request
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            form_data['user_ip'] = x_forwarded_for.split(',')[0]
        else:
            form_data['user_ip'] = self.request.META.get('REMOTE_ADDR')

        # If email me more is selected, add manually values in other fields
        email_me_more = form_data.pop("email_me_more")
        sms_okay = form_data.pop("sms_okay")
        shop_window = form_data.pop("shop_window", None)
        
        form_data['email_me_more'] = 0
        form_data['sms_okay'] = 0
        form_data['disclaimer'] = ""
        form_data['shop_window'] = 0
        # removing extra characters from phone number
        form_data['phone'] = re.sub(r'\D', '', form_data.get('phone', ""))
        
        if email_me_more and email_me_more not in ['0', 0]:
            form_data['email_me_more'] = 1
            form_data['disclaimer'] = "I agree to receive pet & promotional information via the options selected below."
        
        if sms_okay and sms_okay not in ['0', 0]:
            form_data['sms_okay'] = 1
            form_data['disclaimer'] = "I agree to receive pet & promotional information via the options selected below."

        if shop_window and shop_window not in ['0', 0]:
            form_data['shop_window'] = 1
            form_data['email_me_more'] = 1
            form_data['sms_okay'] = 1
            form_data['disclaimer'] = "I consent to being contacted via the channels I have provided ie SMS text message/email etc."

        client.save_lead_conversations(form_data)

        context['success_message'] = "Your request submitted successfully. We'll get back to you shortly."
        context['shopwindow_enable'] = shop_window
        return render(self.request, self.template_name, context=context, status=201)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""

        context = self.get_context_data()
        context['form'] = form
        
        return render(self.request, self.template_name, context=context, status=400)
    


class CustomerVerificationFormMixin(FormView):

    def form_valid(self, form):
        context = self.get_context_data()
        context['form'] = self.form_class
        client = PWAPI()
        
        form_data = form.cleaned_data
        form_data['lead']={}
        form_data['lead']['first_name']=form_data['first_name']
        form_data['lead']['last_name']=form_data['last_name']
        form_data['lead']['email']=form_data['email']
        form_data['lead']['phone']=form_data['phone']

        if form_data.get('first_name'):
            form_data.pop('first_name')
        
        if form_data.get('last_name'):
            form_data.pop('last_name')

        if form_data.get('email'):
            form_data.pop('email')
    
       

        form_data['kind']="Phone"
        form_data['target']=form_data['phone']
        if form_data.get('phone'):
            form_data.pop('phone')
   
        # If email me more is selected, add manually values in other fields

        res=client.consumer_validation(form_data)
        if res.status_code==200:
            self.request.session['consumer_verification_code']=res.json['id']
        else:
            context['error_message']=res.json['error']['message']
        # print(res)
        # context['success_message'] = "Your request submitted successfully. We'll get back to you shortly."
        # context['shopwindow_enable'] = shop_window
        return render(self.request, self.template_name, context=context,status=res.status_code)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""

        context = self.get_context_data()
        context['form'] = form
        
        return render(self.request, self.template_name, context=context, status=400)
    
class OtpVerificationFormMixin(FormView):

    def form_valid(self, form):
        context = self.get_context_data()
        # If email me more is selected, add manually values in other fields
        client = PWAPI()
        form_data = form.cleaned_data

        res=client.consumer_code_verifications(form_data,self.request.session.get('consumer_verification_code'))
        return render(self.request, self.template_name, context=context, status=res.status_code)
    
    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""

        context = self.get_context_data()
        context['form'] = form
        
        return render(self.request, self.template_name, context=context, status=400)

    
class CollectionFormView(CollectionFormMixin):
    
    form_class = CollectionForm
    template_name = 'plugins/includes/general_collection_form.html'

class CustomerVerificationFormView(CustomerVerificationFormMixin):
    
    form_class = CustomerVerificationForm
    template_name = 'plugins/includes/supporting_validation.html'

class OtpVerificationFormView(OtpVerificationFormMixin):
    
    form_class = OtpVerificationForm
    template_name = 'plugins/includes/otp_verification.html'

    
class SubscribeUsFormView(CollectionFormMixin):
    
    form_class = SubscribeUsForm
    template_name = 'plugins/includes/subscribe_us_form.html'

class UnSubscribeUsFormView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            client = PWAPI()
            user_token = client.unsubscribe_marketing_lists(data)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
class MarketingNotification(View):
    def post(self, request, *args, **kwargs):
        try:
            form_data = request.POST
            marketing_list_id = form_data.get('marketing_list')
            name = form_data.get('name')
            email = form_data.get('email')
            user_id = request.user.id
            entity = EntityClient()
            entity.post_marketing_lists(None,marketing_list_id, email )
            return JsonResponse({'success': True, 'status' : 201, "email" : email})
        except Exception as e:
            print("error_MarketingNotification",e)
            return JsonResponse({'error': str(e)}, status=400)
    
class Playdate(View):
    def post(self, request, *args, **kwargs):
        try:
            # Instantiate the form object
            form_obj = SchedulePlaydate(request.POST)
            
            # Check if form is not valid
            if not form_obj.is_valid():
                return HttpResponseBadRequest(json.dumps(form_obj.errors))
            
            # Extract cleaned data from the form
            data = form_obj.cleaned_data

            # Set default values for checkboxes
            data['shop_window'] = int('shop_window' in request.POST)
            data['sms_okay'] = int('sms_okay' in request.POST)
            data['email_me_more'] = int('email_me_more' in request.POST)
            data['reservation'] = int('reservation' in request.POST)

            if data['shop_window'] == 1:
                data['sms_okay'] = 1
                data['email_me_more'] = 1

            # Clean phone number
            data['phone'] = ''.join(filter(str.isdigit, data['phone']))
            
            # Get additional data from request
            start_at = request.POST.get('start_at', '')
            finish_at = request.POST.get('finish_at', '')
            location_id = int(request.POST.get('location_id', ''))

            # Format phone number if it has 10 digits
            if len(data['phone']) == 10:
                data['phone'] = f"+1{data['phone']}"

            # Create PWAPI client and make API call
            client = PWAPI()
            client.create_pet_box_visit(
                pet_id=int(data['pet_id']),
                start_at=start_at,
                finish_at=finish_at,
                email=data['email'],
                phone=data['phone'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                location_id=location_id,
                shop_window=data['shop_window'],
                sms_okay=data['sms_okay'],
                email_me_more=data['email_me_more'],
                reservation=data['reservation'],
                notes='',
            )

            # Return success response
            return JsonResponse({'message': 'Successfully created.'}, status=201)
        except Exception as e:
            # Return error response if any exception occurs
            return JsonResponse({'error': str(e)}, status=500)

class AvailablePuppyCollectionFormView(CollectionFormMixin):

    form_class = AvailablePuppyCollectionForm
    template_name = 'plugins/includes/available_puppy_collection_form.html'


class PlayDateCreateView(View):
     
    form_class = SchedulePlaydate
    template_name = 'plugins/includes/schedule_a_Playdate.html'

    @staticmethod
    def get(self, request, *args, **kwargs):
        #FIXME: Complete this or remove if this is not used
        location_id = kwargs.get('location_id', None)
        if not location_id:
            raise Http404()
        start_at = datetime.date.today()
        finish_at = start_at + datetime.timedelta(days=3)

        client = PWAPI()
        r = client.get_pet_box_visits_schedule(start_at=start_at, finish_at=finish_at, location_id=location_id)
        result = r.get('objects', [])
        if result:
            data_filtered = []
            now = datetime.datetime.now(pytz.utc)
            for item in result:
                start_at = parse_datetime(item['start_at'])
                if start_at < now:
                    continue
                data_filtered.append(item)
            result = data_filtered

    @staticmethod
    def post(request):
        try:
            # Instantiate the form object
            form_obj = SchedulePlaydate(request.POST)
            
            # Check if form is not valid
            if not form_obj.is_valid():
                return HttpResponseBadRequest(json.dumps(form_obj.errors))
            
            # Extract cleaned data from the form
            data = form_obj.cleaned_data

            # Set default values for checkboxes
            data['shop_window'] = int('shop_window' in request.POST)
            data['sms_okay'] = int('sms_okay' in request.POST)
            data['email_me_more'] = int('email_me_more' in request.POST)
            data['reservation'] = int('reservation' in request.POST)

            if data['shop_window'] == 1:
                data['sms_okay'] = 1
                data['email_me_more'] = 1

            # Clean phone number
            data['phone'] = ''.join(filter(str.isdigit, data['phone']))
            
            # Get additional data from request
            start_at = request.POST.get('start_at', '')
            finish_at = request.POST.get('finish_at', '')
            location_id = int(request.POST.get('location_id', ''))

            # Format phone number if it has 10 digits
            if len(data['phone']) == 10:
                data['phone'] = f"+1{data['phone']}"

            # Create PWAPI client and make API call
            client = PWAPI()
            client.create_pet_box_visit(
                pet_id=int(data['pet_id']),
                start_at=start_at,
                finish_at=finish_at,
                email=data['email'],
                phone=data['phone'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                location_id=location_id,
                shop_window=data['shop_window'],
                sms_okay=data['sms_okay'],
                email_me_more=data['email_me_more'],
                reservation=data['reservation'],
                notes='',
            )

            # Return success response
            return JsonResponse({'message': 'Successfully created.'}, status=201)
        except Exception as e:
            # Return error response if any exception occurs
            return JsonResponse({'error': str(e)}, status=500)


class CheckZipView(View):

    def get(self, request, *args, **kwargs):
        code, state = request.GET.get('zip'), request.GET.get('state')
        if not code or not state:
            return HttpResponse(status=400)
        
        try:
            country = int(request.GET.get('country', 231))
        except ValueError:
            return HttpResponse(status=400)

        result = False

        if country == 231:
            try:
                with SearchEngine() as search:
                    state_data = search.by_zipcode(code)
                    result = state_data and state_data.state == state
            except Exception as e:
                result = False
        elif country == 38:
            pattern = "^[ABCEGHJKLMNPRSTVXY]{1}[0-9]{1}[A-Z]{1} ?[0-9]{1}[A-Z]{1}[0-9]{1}$"
            result = re.match(pattern, code)
        elif country == 142:
            pattern = "^[0-9]{5}$"
            result = re.match(pattern, code)

        return HttpResponse(status=200 if result else 400)


class HeaderDeleteView(View):

    def delete(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        deleted_img = ThemeImages.objects.filter(id=json_data["image_id"]).delete()
        if deleted_img:
            return HttpResponse(
                json.dumps(
                    {
                        "message": "Image deleted succesfully",
                    }
                ),
                status=200,
            )
        else:
            return HttpResponse(
                json.dumps(
                    {
                        "message": "Something went wrong.",
                    }
                ),
                status=400,
            )

def google_maps_proxy(request):
    response = cache.get("google_map_response")
    if response is None:
        endpoint = "https://maps.googleapis.com/maps/api/js"
        params = {
            'key': settings.GOOGLE_REVIEWS_KEY,
            'libraries': request.GET.get('libraries', 'places'),
            'callback': request.GET.get('callback', 'initMap'),
        }
        
        response = requests.get(endpoint, params=params)
        #caching for 1 year
        cache.set("google_map_response", response, 60 * 60 * 24 * 365)
    return HttpResponse(response.content, content_type='application/javascript')


