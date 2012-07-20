# Author Samvit Majumdar <samvit.1@gmail.com>
from django import forms
import re
from cms.conference.models import Payment

class PaymentForm(forms.ModelForm):
  class Meta:
    model = Payment
    exclude = ('transaction_id','verified','payment_from','time')

  