from django import forms
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from src.models.refund import Refund
from src.models.profile import Profile
from src.models.contact import Contact


PAYMENT_OPTION = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
    ('M', 'Mpesa')
)


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(required=False,
                                                                              widget=CountrySelectWidget(attrs={
                                                                                  'class': 'custom-select d-block w-100'
                                                                              }))
    shipping_zip = forms.CharField(required=False)
    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(required=False,
                                                                             widget=CountrySelectWidget(attrs={
                                                                                 'class': 'custom-select d-block w-100'
                                                                             }))
    billing_zip = forms.CharField(required=False)
    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_OPTION)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promotion code',
        'aria - label': "Recipient's username",
        'aria - describedby': "basic-addon2"
    }))


class RefundForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = ['ref_code', 'reason']
        widgets = {
            'ref_code': forms.TextInput(attrs={
                'placeholder': 'Enter reference code.'
            }),
            'reason': forms.Textarea(attrs={'class': 'input', 'placeholder': 'Enter reason.'})
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'phone_number', 'country']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Enter phone number'
            }),
            'country': CountrySelectWidget(attrs={'class': 'custom-select d-block w-100'}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your username'}),
            'email': forms.TextInput(
                attrs={'class': 'input', 'placeholder': 'Enter your email address', 'type': 'email'})
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'input', 'placeholder': 'Enter your message'}),

        }


