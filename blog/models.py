from django.db import models


class Post(models.Model):
    statuses = (
        ("moderation", "moderation"),
        ("active", "active"),
    )

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(auto_now=True)
    img = models.ImageField(null=True, blank=True, upload_to='images')
    status = models.CharField(choices=statuses, default="moderation", max_length=10)
    def __str__(self):
        return self.title

