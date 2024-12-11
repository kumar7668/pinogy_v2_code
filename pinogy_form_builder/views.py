from django.http import JsonResponse
from django.views import View
from .forms import formBuilder
from common_plugins import utils
from pos_api.pos_client import PWAPI
import re


class BuilderFormSubmitView(View):
    def post(self, request, *args, **kwargs):
        form = formBuilder(request.POST)
        if form.is_valid():
            client = PWAPI()
            form_data = {}
            # Get user's IP address from the request
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                form_data['user_ip'] = x_forwarded_for.split(',')[0]
            else:
                form_data['user_ip'] = request.META.get('REMOTE_ADDR')

            store_data = utils.get_stores_data(client=client)
            default_store_id = None
            if len(store_data) > 0:
                default_store_id = store_data[0].get('id',None)
            store_id = request.session.get('store_location_id') or \
                request.COOKIES.get('store_location_id') or default_store_id
            
            form_data['location_id'] = str(store_id)
            form_data['shop_window'] = 0
            form_data['sms_okay'] = 0
            form_data['email_me_more'] = 0
            for key, values in self.request.POST.lists():
                # Remove csrf and captcha value from the form data
                if key not in ['csrfmiddlewaretoken', 'g-recaptcha-response']:
                    # handling checkbox field here
                    if len(values) == 1:
                        form_data[key] = self.get_valid_value(values)[0]
                        # set sms_okay and email_me_more if shop_window is enabled
                        if key == 'shop_window':
                            form_data['sms_okay'] = 1
                            form_data['email_me_more'] = 1
                        if key == 'phone':
                            form_data[key] = re.sub(r'\D', '', values[0])

                    else:
                        form_data[key] = self.get_valid_value(values)

            client.save_lead_conversations(form_data)
            return JsonResponse({'status': 'success', 'message': 'Form submitted successfully'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Form validation failed'}, status=400)

    def get_valid_value(self,values):
        values_list = []
        for value in values:
            # if checkbox is on then change value to 1
            if value == 'on':
                values_list.append(1)
            # if checkbox is off then change value to 0  
            elif value == 'off':
                values_list.append(0)
            else:
                if value == '0' or value == '1':
                   values_list.append(int(value))
                else:
                    values_list.append(value)

        return values_list
        


