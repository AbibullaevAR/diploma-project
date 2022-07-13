from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.contrib.auth.models import User, Permission

from .models import Profile, Group


class MentorRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    group = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = user.email

        if commit:
            user.save()
            permission = Permission.objects.get(codename='mentor')
            user.user_permissions.add(permission)

            group = Group(group_name=self.cleaned_data['group'])
            group.save()

            user_profile = Profile()
            user_profile.user = user
            user_profile.group = group
            user_profile.save()
        return user
