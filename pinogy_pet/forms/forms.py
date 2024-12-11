from django.utils.translation import gettext_lazy as _
from django import forms

from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class PetPurchaseUserForm(forms.Form):

    first_name = forms.CharField(label=_("First Name"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control', 'aria-label': 'First Name', 'autocomplete': 'given-name'})
    )
    last_name = forms.CharField(label=_("Last Name"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control', 'aria-label': 'Last Name', 'autocomplete': 'given-name'})
    )
    email = forms.EmailField(label=_("Email"), required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control', 'aria-label': 'email', 'autocomplete': 'email'})
    )
    phone = forms.CharField(label=_("Phone Number"), max_length=17, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number', 'class': 'form-control phone-validation', 'aria-label': 'Phone Number', 'autocomplete': 'tel'}),
    )
    address = forms.CharField(label=_("Address"), max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control', 'aria-label': 'Address 1', 'autocomplete': 'given-name'})
    )
    address_2 = forms.CharField(label=_("Address 2"), max_length=100, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Address 2', 'class': 'form-control', 'aria-label': 'Address 2', 'autocomplete': 'given-name'})
    )
    city = forms.CharField(label=_("City"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control', 'aria-label': 'City', 'autocomplete': 'given-name'})
    )
    zip = forms.CharField(label=_("Zip"), max_length=6, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Zip', 'class': 'form-control', 'aria-label': 'Zip Code', 'autocomplete': 'postal-code'}),
    )
    state = forms.CharField(label=_("State"), max_length=6, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control', 'aria-label': 'State', 'autocomplete': 'given-name'}),
    )
    email_me_more = forms.BooleanField(required=False)
    sms_okay = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(PetPurchaseUserForm, self).__init__(*args, **kwargs)


class PetPaymentForm(forms.Form):

    txn_id = forms.IntegerField(label=_("Txn Id"), required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Txn Id', 'class': 'form-control', 'aria-label': 'Transaction id', 'autocomplete': 'given-name'})
    )
    card_holder = forms.CharField(label=_("Card Holder"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Card Holder', 'class': 'form-control', 'aria-label': 'Card Holder Name', 'autocomplete': 'given-name'})
    )
    email = forms.EmailField(label=_("Email"), required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control', 'aria-label': 'Email', 'autocomplete': 'email'})
    )
    card_token = forms.CharField(label=_("Card Token"), max_length=30, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Card Token', 'class': 'form-control'}),
    )
    card_expiry = forms.CharField(label=_("Card Expiry"), max_length=10, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Card Expiry', 'class': 'form-control'})
    )
    card_method = forms.ChoiceField(label=_("Card Method"), choices=[], required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Card Method', 'class': 'form-control'})
    )
    deposit_amount = forms.FloatField(label=_("Deposit Amount"), required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Deposit Amount', 'class': 'form-control'})
    )
    is_deposit = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(PetPaymentForm, self).__init__(*args, **kwargs)

        self.fields['card_method'].choices = [
            ("-6", "-6"),
            ("-7", "-7"),
            ("-8", "-8"),
            ("-9", "-9"),
            ("-10", "-10"),
        ]


class PetCollectionForm(forms.Form):
    
    first_name = forms.CharField(label=_("First Name"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control', 'aria-label': 'First Name', 'autocomplete': 'given-name'})
    )
    last_name = forms.CharField(label=_("Last Name"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control', 'aria-label': 'Last Name', 'autocomplete': 'given-name'})
    )
    email = forms.EmailField(label=_("Email"), required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control', 'aria-label': 'Email', 'autocomplete': 'email'})
    )
    phone = forms.CharField(label=_("Phone Number"), max_length=17, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number', 'class': 'form-control phone-validation', 'aria-label': 'Phone Number', 'autocomplete': 'tel'}),
    )
    message = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 5, 'placeholder': 'Enter message here', 'class': 'form-control focus-color', 'aria-label': 'message', 'autocomplete': 'given-name'}
    ), required=False)
    
    pet_id = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    pet_gender = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    breed = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False) # name 
    breed_slug = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    pet_type_slug = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    location_id = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    location = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False) # name
    
    email_me_more = forms.BooleanField(required=False)
    sms_okay = forms.BooleanField(required=False)
    shop_window = forms.BooleanField(required=False)
    
    form = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=True)
    site_url = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=True)
    page_referer = forms.CharField(widget=forms.HiddenInput(), max_length=100, required=True)

    captcha = ReCaptchaField(error_messages = {'required': "Captcha is required"})