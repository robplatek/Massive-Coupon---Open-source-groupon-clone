from django import forms
from django.forms import widgets
from massivecoupon.engine import models as enginemodels
from massivecoupon.libs import formutils
from datetime import date
import re
import pdb

r_postalcode = re.compile(r'^([A-Z][0-9][A-Z])[ -]?([0-9][A-Z][0-9])$', re.I)
r_date = re.compile(r'^(\d\d\d\d)[/-](\d{1,2})[/-](\d{1,2})$')

expiry_choices_month = (
  (1, '1'),
  (2, '2'),
  (3, '3'),
  (4, '4'),
  (5, '5'),
  (6, '6'),
  (7, '7'),
  (8, '8'),
  (9, '9'),
  (10, '10'),
  (11, '11'),
  (12, '12'),
)

expiry_choices_year = (
  (2010, '2010'),
  (2011, '2011'),
  (2012, '2012'),
  (2013, '2013'),
  (2014, '2014'),
  (2015, '2015'),
  (2016, '2016'),
  (2017, '2017'),
  (2018, '2018'),
  (2019, '2019'),
  (2020, '2020'),
)

class EmailSubForm(forms.Form):
    email               = forms.EmailField(help_text="you@domain.com", widget=forms.TextInput(attrs={'size':'25'}))
    city                = forms.ChoiceField(initial=1, choices=[ (obj.id, obj.name) for obj in enginemodels.City.objects.all() ])


class SignupForm(forms.Form):
  full_name           = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'size':'30'}) )
  password            = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'size':'12'}) )
  password_verify     = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'size':'12'}))
  email               = forms.EmailField(help_text="you@domain.com", widget=forms.TextInput(attrs={'size':'30'}))


  def clean(self):
    """
    Validate fields to make sure everything's as expected.
    - postalcode is in right format and actually exists
    - service actually exists
    """
    cd = self.cleaned_data

    if 'password' in cd and 'password_verify' in cd:
      if self.cleaned_data['password'] != self.cleaned_data['password_verify']:
        self._errors['password'] = forms.util.ErrorList(["Passwords don't match!"])

    else:
      self._errors['password'] = forms.util.ErrorList(["Please enter and confirm your password"])

#      raise forms.ValidationError(_(u'Please enter and confirm your password'))


    return cd



class LoginForm(forms.Form):
    email               = forms.EmailField(help_text="you@domain.com", widget=forms.TextInput(attrs={'size':'25'}))
    password            = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'size':'12'}) )

    def clean(self):
        # only do further checks if the rest was valid
        if self._errors: return
            
        from django.contrib.auth import login, authenticate
        user = authenticate(username=self.data['email'],
                                password=self.data['password'])
        if user is not None:
            if user.is_active:
                self.user = user                    
            else:
                raise forms.ValidationError( 'This account is currently inactive. Please contact the administrator if you believe this to be in error.')
        else:
            raise forms.ValidationError( 'The username and password you specified are not valid.')


class DealCheckoutForm(forms.Form):

  full_name           = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'size':'30'}) )
  password            = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'size':'12'}) )
  password_verify     = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'size':'12'}))
  email               = forms.EmailField(help_text="you@domain.com", widget=forms.TextInput(attrs={'size':'30'}))

  quantity            = forms.IntegerField(initial=1, widget=forms.TextInput(attrs={'size':'2'}))

#  cardholder_name     = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'size':'30'}))
#  type                = forms.ChoiceField( choices = enginemodels.CC_TYPE )
#  number              = forms.CharField(help_text="Enter your credit card #", max_length=20)
#  expiry_month        = forms.ChoiceField(choices=expiry_choices_month, help_text="Enter your credit card expiration month")
#  expiry_year         = forms.ChoiceField(choices=expiry_choices_year, help_text="Enter your credit card expiration year")
#  security            = forms.CharField(help_text="CVV", max_length=5, widget=forms.TextInput(attrs={'size':'5'}))
#  billing_address     = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'size':'30'}))
#  city                = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'size':'30'}))
#  postalcode          = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'size':'7'}))
#  province            = forms.ChoiceField(choices=enginemodels.PROVINCES)
#  country             = forms.ChoiceField(initial="CA", choices=[ (obj.iso, obj.name) for obj in enginemodels.Country.objects.all() ])

  def clean(self):
    """
    Validate fields to make sure everything's as expected.
    - postalcode is in right format and actually exists
    - service actually exists
    """
    cd = self.cleaned_data

    if 'password' in cd and 'password_verify' in cd:
      if self.cleaned_data['password'] != self.cleaned_data['password_verify']:
        self._errors['password'] = forms.util.ErrorList(["Passwords don't match!"])

    else:
      self._errors['password'] = forms.util.ErrorList(["Please enter and confirm your password"])

#      raise forms.ValidationError(_(u'Please enter and confirm your password'))


    return cd

