from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .models import Post
from .models import Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'category', 'slug', 'img')  # попробуй сюда добавить img


class AuthForm(forms.Form):
    username = forms.SlugField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        if user is None:
            raise ValidationError('username or password is invalid')

        self.cleaned_data['user'] = user

        return self.cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'parent')


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'about')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'about')
