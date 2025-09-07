from django.contrib import admin
from .models import Post, Like, Comment, Share, Category

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'published', 'category')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('category',) # Add category to the list filter

# Add these admin classes
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at', 'active']
    list_filter = ['created_at', 'active']
    search_fields = ['content', 'author__username']
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(active=True)
        self.message_user(request, f'{queryset.count()} comments approved.')
    
    def disapprove_comments(self, request, queryset):
        queryset.update(active=False)
        self.message_user(request, f'{queryset.count()} comments disapproved.')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'shared_at']
    list_filter = ['shared_at']

# Register the Category model to appear in the admin panel
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']