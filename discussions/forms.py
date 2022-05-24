from django import forms
from django.core import validators

from .models import Discussions

class DiscussionForm(forms.ModelForm):

    class Meta:
        model = Discussions
        fields = ()
