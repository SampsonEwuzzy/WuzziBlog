from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import logout

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately
            return redirect('posts:home')
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('posts:home')