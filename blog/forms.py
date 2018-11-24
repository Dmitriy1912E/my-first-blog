from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)


class AuthForm(forms.Form):
    username = forms.SlugField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        if user is None:
            raise ValidationError('username or password is invalid')

        self.cleaned_data['user'] = user

        return self.cleaned_data
