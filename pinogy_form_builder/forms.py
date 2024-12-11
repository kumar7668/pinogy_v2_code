from django import forms
from django.utils.translation import gettext_lazy as _
from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from .models import MarketingFieldPluginModel
from common_plugins import utils
from pos_api.pos_client import PWAPI
class formBuilder(forms.Form):
    captcha = ReCaptchaField(error_messages={'required': "Captcha is required"})

    def __init__(self, *args, **kwargs):
        super(formBuilder, self).__init__(*args, **kwargs)

class MarketingFieldPluginForm(forms.ModelForm):
    # Custom field for default_location with dynamic choices
    default_location = forms.ChoiceField(
        choices=[],
        label="Select Default Location",
        help_text="Choose a marketing location from the list",
        required=False
    )

    class Meta:
        model = MarketingFieldPluginModel
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Fetch API data and set choices for the custom default_location field
        self.fields['default_location'].choices = self.fetch_api_data()

    def fetch_api_data(self):
        try:
            client = PWAPI()
            api_stores = utils.get_stores_data(client=client)
            choices = [(store['id'], store['receipt_name']) for store in api_stores]
        except Exception as e:
            choices = []

        return choices
