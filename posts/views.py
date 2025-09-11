from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import Post, Like, Comment, Share, Category
from .forms import RegisterForm, PostForm, CommentForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.db.models import Q
from .forms import PhotoForm
from .models import Photo

def home(request):
    latest_posts = Post.objects.filter(published=True).order_by("-created_at")[:4]
    return render(request, "posts/home.html", {"latest_posts": latest_posts})

def about(request):
    return render(request, "posts/about.html")

def post_list(request):
    posts = Post.objects.filter(published=True).order_by("-created_at")
    categories = Category.objects.all()
    return render(request, "posts/post_list.html", {
        "posts": posts,
        "categories": categories,
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    context = {"post": post}
    extra_context = get_post_context(request, post)
    context.update(extra_context)
    return render(request, "posts/post_detail.html", context)

@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect("posts:post_detail", slug=post.slug)
    else:
        form = PostForm()
    return render(request, "posts/post_form.html", {"form": form})

@login_required
def upload_photo(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("gallery")
    else:
        form = PhotoForm()
    return render(request, "upload.html", {"form": form})

def gallery(request):
    photos = Photo.objects.all()
    return render(request, "gallery.html", {"photos": photos})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("posts:home")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to WuzziBlog.")
            return redirect("posts:home")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})

@login_required
@require_POST
def toggle_like(request, slug):
    post = get_object_or_404(Post, slug=slug)

    try:
        user_like = Like.objects.filter(user=request.user, post=post)

        if user_like.exists():
            user_like.delete()
            liked = False
            message = "Post unliked"
        else:
            Like.objects.create(user=request.user, post=post)
            liked = True
            message = "Post liked"

        total_likes = post.likes.count()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "success": True,
                "liked": liked,
                "total_likes": total_likes,
                "message": message,
            })

        messages.success(request, message)
        return redirect("posts:post_detail", slug=post.slug)

    except Exception as e:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "error": str(e)})
        messages.error(request, "Error processing like")
        return redirect("posts:post_detail", slug=post.slug)

@login_required
@require_POST
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)

    try:
        content = request.POST.get("content", "").strip()
        if not content:
            messages.error(request, "Comment cannot be empty")
            return redirect("posts:post_detail", slug=post.slug)

        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
            active=True,
        )

        parent_id = request.POST.get("parent_id")
        if parent_id:
            try:
                parent_comment = Comment.objects.get(id=parent_id)
                comment.parent = parent_comment
                comment.save()
                messages.success(request, "Reply added successfully!")
            except Comment.DoesNotExist:
                messages.error(request, "Parent comment not found")
        else:
            messages.success(request, "Comment added successfully!")

        return redirect("posts:post_detail", slug=post.slug)

    except Exception as e:
        messages.error(request, f"Error adding comment: {str(e)}")
        return redirect("posts:post_detail", slug=post.slug)

@login_required
def share_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    try:
        share, created = Share.objects.get_or_create(user=request.user, post=post)

        if created:
            messages.success(request, f'You shared "{post.title}"!')
        else:
            messages.info(request, "You have already shared this post.")

        post_url = request.build_absolute_uri(
            reverse("posts:post_detail", kwargs={"slug": post.slug})
        )
        request.session["shared_post"] = {
            "title": post.title,
            "url": post_url,
            "facebook_url": f"https://www.facebook.com/sharer/sharer.php?u={post_url}",
            "twitter_url": f"https://twitter.com/intent/tweet?url={post_url}&text={post.title}",
            "whatsapp_url": f"https://wa.me/?text={post.title} {post_url}",
        }

        return redirect("posts:post_detail", slug=post.slug)

    except Exception as e:
        messages.error(request, f"Error sharing post: {str(e)}")
        return redirect("posts:post_detail", slug=post.slug)

def get_post_context(request, post):
    context = {}

    if request.user.is_authenticated:
        context["user_has_liked"] = Like.objects.filter(user=request.user, post=post).exists()
    else:
        context["user_has_liked"] = False

    context["comments"] = post.comments.filter(active=True, parent=None).order_by("-created_at")
    context["comment_form"] = CommentForm()
    context["shared_post"] = request.session.pop("shared_post", None)

    return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post updated successfully!")
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse("posts:post_detail", kwargs={"slug": self.object.slug})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"
    success_url = reverse_lazy("posts:list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def post(self, request, *args, **kwargs):
        messages.success(request, "Post deleted successfully!")
        return super().post(request, *args, **kwargs)

def search_posts(request):
    query = request.GET.get("q")
    results = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    ).distinct()
    return render(request, "posts/search_results.html", {"results": results, "query": query})

def category_posts(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    posts = Post.objects.filter(category=category).order_by("-created_at")
    return render(request, "posts/post_list.html", {"posts": posts})
