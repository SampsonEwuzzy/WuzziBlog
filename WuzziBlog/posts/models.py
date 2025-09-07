from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField 
from django.urls import reverse

# Corrected Models
# Define the Category model first so other models can reference it.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = RichTextUploadingField(config_name='default') 
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, max_length=2000)
    image_caption = models.CharField(max_length=255, blank=True) # Add this field
    # The 'likes' field is a ManyToManyField on the Post model
    likes = models.ManyToManyField(User, related_name='liked_posts', through='Like', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def total_likes(self):
        # This correctly counts the users in the ManyToManyField
        return self.likes.count()

    def total_comments(self):
        # Correctly uses the related_name 'comments' from the Comment model
        return self.comments.filter(active=True).count()

    def total_shares(self):
        # Correctly uses the related_name 'shares' from the Share model
        return self.shares.count()

# The Like model creates a reverse relationship.
# This caused a clash with the Post.likes field.
# The fix is to add a unique related_name to the ForeignKey.
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # FIX: Remove 'related_name' to allow Post.likes to correctly manage the relationship.
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
    
    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def get_replies(self):
        return Comment.objects.filter(parent=self, active=True)

class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='shares', on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} shared {self.post.title}'