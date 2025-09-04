from django.urls import path
from . import views

# Removed app_name = 'posts' to eliminate namespace

urlpatterns = [
    path("", views.home, name="home"),                # homepage
    path("about/", views.about, name="about"),        # about page

    # Posts
    path("posts/", views.post_list, name="posts"),    # list all posts
    path("posts/<int:pk>/", views.post_detail, name="post_detail"),  # view post details
    path("posts/new/", views.add_post, name="add_post"),
        # Auth
    path("register/", views.register, name="register"),
]