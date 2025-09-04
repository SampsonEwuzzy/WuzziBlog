from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    image = models.ImageField(upload_to="post_images/", blank=True, null=True) 

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title