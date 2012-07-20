# Author Samvit Majumdar <samvit.1@gmail.com>
from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from submission.models import Submission,Comments

class SubmissionForm(forms.ModelForm):
  class Meta:
    model = Submission
    widgets = {
            'topic':   CheckboxSelectMultiple,
        }
  

class CommentsForm(forms.ModelForm):
  class Meta:
    model = Comments
#    exclude = ('author')