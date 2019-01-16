from django.contrib import admin
from django.contrib.auth.models import User

from .models import Post, Category

admin.site.register(Post)
admin.site.register(Category)


User.objects.get_or_create(username='test', defaults={
    'password': 'qwfqwfqwf'
})