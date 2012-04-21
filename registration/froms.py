# Author Samvit Majumdar <samvit.1@gmail.com>

from django import forms
import re
from django.contrib.auth.models import User
from cms.registration.models import USER_TYPES

class SignUpForm(forms.Form):
  username = forms.CharField(max_length=100)
  password = forms.CharField(max_length=100,widget=forms.PasswordInput)
  re_password = forms.CharField(max_length=100,label='Re enter Password',widget=forms.PasswordInput)
  first_name = forms.CharField(max_length=100)
  last_name = forms.CharField(max_length=100)
  email = forms.EmailField()
  city = forms.CharField(max_length=100)
  phone = forms.CharField(max_length=100)
  country = forms.CharField(max_length=100)
  type = forms.ChoiceField(choices=USER_TYPES,label='I am a(n) ')

  def clean_username(self):
    data = self.cleaned_data['username']
    user = User.objects.filter(username = data)
    if user:
      raise forms.ValidationError("Username already taken!")
    if not len(data):
      raise forms.ValidationError("Username cannot be empty")
    match = re.match(r'[a-z_\.\d]+',data)
    if match:
      if len(data) != len(match.group()):
        raise forms.ValidationError('Username can only consist of a-z, _ and .')
      if len(match.group())<6:
        raise forms.ValidationError('Username should be greater that 5 characters')
    else:
      raise forms.ValidationError('Username can only consist of a-z, "_" and ". "')
    return data

  def clean_re_password(self):
    p = self.cleaned_data['password']
    rp = self.cleaned_data['re_password']
    if not p == rp:
      raise forms.ValidationError("Passwords do not match")
    return rp

  def clean_phone(self):
    p = self.cleaned_data['phone']
    match = re.match(r'\d+',p)
    if match:
      if len(match.group()) > 10 or len(match.group()) < 10:
        raise forms.ValidationError('Please enter a 10 digit number')
    else:
      raise forms.ValidationError('Please enter only digits in this field')
    return p



    
  