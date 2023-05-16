from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Post, Follower, Like, User
from .forms import NewPostForm

def index(request):
    posts = Post.objects.all().order_by('-date')
    # function to display new post form and save to db
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            # Get all data from the form
            user = User.objects.get(pk=request.user.id)
            content = form.cleaned_data["content"]
            post = Post(
                user = user,
                content=content
            )
            post.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "network/index.html",{
                "form": form
            })      
    return render(request, "network/index.html", {
        "form": NewPostForm(),
        "posts": posts,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def display_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(user=user).order_by('-date')
    followers = Follower.objects.filter(user_followed=user)
    following = Follower.objects.filter(user_following=user)
    return render(request, "network/profile.html", {
        "user": user,
        "posts": posts,
        "following": following,
        "followers": followers
    })

