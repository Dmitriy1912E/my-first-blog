from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import DateTimeField
from django.conf import settings


class Tag(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    slug = models.CharField(max_length=30, verbose_name="Tags")

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['slug']

    def __str__(self):
        return self.slug


class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    title = models.CharField(max_length=255, verbose_name="Title")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title


class Post(models.Model):
    statuses = (
        ("moderation", "moderation"),
        ("active", "active"),
    )

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts')
    slug = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(auto_now=True)
    img = models.ImageField(null=True, blank=True, upload_to='images')
    status = models.CharField(choices=statuses, default="moderation", max_length=10)

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


