from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'posts'

urlpatterns = [
    # Core pages
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),

    # Posts
    path("posts/", views.post_list, name="list"),
    path("posts/new/", views.add_post, name="new_post"),
    path("posts/<slug:slug>/", views.post_detail, name="post_detail"),
    path("posts/edit/<slug:slug>/", views.PostUpdateView.as_view(), name="edit_post"),
    path("posts/delete/<slug:slug>/", views.PostDeleteView.as_view(), name="delete_post"),

    # Post Actions (slug-based)
    path("toggle-like/<slug:slug>/", views.toggle_like, name="toggle_like"),
    path("add-comment/<slug:slug>/", views.add_comment, name="add_comment"),
    path("share-post/<slug:slug>/", views.share_post, name="share_post"),

    # Other
    path("search/", views.search_posts, name="search"),
    path("category/<str:category_name>/", views.category_posts, name="category_posts"),

     # Password reset
    path("password-reset/", 
         auth_views.PasswordResetView.as_view(template_name="posts/password_reset.html"), 
         name="password_reset"),
    path("password-reset/done/", 
         auth_views.PasswordResetDoneView.as_view(template_name="posts/password_reset_done.html"), 
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(template_name="posts/password_reset_confirm.html"), 
         name="password_reset_confirm"),
    path("reset/done/", 
         auth_views.PasswordResetCompleteView.as_view(template_name="posts/password_reset_complete.html"), 
         name="password_reset_complete"),
     path("upload/", views.upload_photo, 
          name="upload"),
    path("gallery/", views.gallery, 
          name="gallery"), 

]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
