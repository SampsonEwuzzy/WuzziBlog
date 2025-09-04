from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import Post
from .forms import RegisterForm,PostForm


def home(request):
    latest_posts = Post.objects.filter(published=True).order_by("-created_at")[:4]
    return render(request, "posts/home.html", {"latest_posts": latest_posts})


def about(request):
    return render(request, "posts/about.html")


def post_list(request):
    posts = Post.objects.filter(published=True).order_by("-created_at")
    return render(request, "posts/post_list.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, published=True)
    return render(request, "posts/post_detail.html", {"post": post})


@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
    return render(request, "posts/add_post.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log the user in after registration
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "posts/register.html", {"form": form})
