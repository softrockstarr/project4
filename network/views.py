from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
import json 

from .models import Post, Follower, Like, User
from .forms import NewPostForm

def index(request):
    posts = Post.objects.all().order_by('-date')
    # pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

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
    # modify likes          
    likes = Like.objects.all()
    liked_posts = []

    try: 
        for like in likes:
            if like.user.id == request.user.id:
                liked_posts.append(like.post.id)
    except:
        liked_posts = []     

    return render(request, "network/index.html", {
        "form": NewPostForm(),
        "posts": posts,
        "page_obj": page_obj,
        "liked_posts": liked_posts,
        "likes": likes
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
    is_follower = followers.filter(user_following=request.user)
    user_is_following = len(is_follower) > 0
    # pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # modify likes          
    likes = Like.objects.all()
    liked_posts = []

    try: 
        for like in likes:
            if like.user.id == request.user.id:
                liked_posts.append(like.post.id)
    except:
        liked_posts = []     
        
    return render(request, "network/profile.html", {
        "user": user,
        "posts": posts,
        "following": following,
        "followers": followers,
        "is_following": user_is_following,
        "current_user": request.user.id,
        "page_obj": page_obj,
        "liked_posts": liked_posts,
        "likes": likes
    })


def follow(request):
    user_follow = request.POST['userfollow']
    current_user = User.objects.get(pk=request.user.id)
    user_follow_data = User.objects.get(username=user_follow)
    follow = Follower(
        user_following=current_user, 
        user_followed=user_follow_data
        )
    follow.save()
    user_id = user_follow_data.id
    return HttpResponseRedirect(reverse(display_profile, kwargs={'id': user_id}))


def unfollow(request):
    user_follow = request.POST['userfollow']
    current_user = User.objects.get(pk=request.user.id)
    user_follow_data = User.objects.get(username=user_follow)
    follow = Follower.objects.get(
        user_following=current_user, 
        user_followed=user_follow_data
        )
    follow.delete()
    user_id = user_follow_data.id
    return HttpResponseRedirect(reverse(display_profile, kwargs={'id': user_id}))

def following(request):
    current_user = User.objects.get(pk=request.user.id)
    following = Follower.objects.filter(user_following=current_user)
    all_posts = Post.objects.all().order_by('-date')
    following_posts = []

    for post in all_posts:
        for person in following:
            if person.user_followed == post.user:
                following_posts.append(post) 

    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # modify likes          
    likes = Like.objects.all()
    liked_posts = []

    try: 
        for like in likes:
            if like.user.id == request.user.id:
                liked_posts.append(like.post.id)
    except:
        liked_posts = []     

    return render(request, "network/following.html", {
        "posts": all_posts,
        "page_obj": page_obj,
        "liked_posts": liked_posts,
        "likes": likes
    })

def edit_post(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        post = Post.objects.get(pk=post_id)
        post.content = data["content"]
        post.save()
        return JsonResponse({"message": "edit successful", "data": data["content"]})
    
def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like(user=user, post=post)
    like.save()
    return JsonResponse({"message": "post liked"})

def unlike(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like.objects.filter(user=user, post=post)
    like.delete()
    return JsonResponse({"message": "post unliked"})



