from django import forms
from django.core import validators

from .models import NewsModel


class CreateNewsForm(forms.ModelForm):

    tags = forms.CharField(validators=[validators.RegexValidator(r'#[-a-zA-Z0-9_]+')])

    class Meta:
        model = NewsModel
        fields = ('title', 'body')
