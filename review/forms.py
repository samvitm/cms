# Author Samvit Majumdar <samvit.1@gmail.com>

from django.forms import ModelForm
from django.forms.fields import ChoiceField
from django.forms.models import ModelChoiceField
from django.forms.widgets import RadioSelect
from review.models import Review, Recomendation
from review.models import RATING_CHOICES
class ReviewForm(ModelForm):
  recomendation = ModelChoiceField(Recomendation.objects.all(), empty_label=None,widget=RadioSelect,)
  overall_rating = ChoiceField(RATING_CHOICES,widget=RadioSelect)
  class Meta:
    model = Review
    widgets = {
            'recomendation': RadioSelect,
            'overall_rating': RadioSelect
        }