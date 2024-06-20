import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from .models import Posting, Follow, Like
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User



def index(request):
    if request.user.is_authenticated:
        
        followed_users = Follow.objects.filter(user=request.user).values_list('profile_user', flat=True)
        posts_list = Posting.objects.order_by('-created_at')
    else:
        posts_list = Posting.objects.all().order_by('-created_at')

    paginator = Paginator(posts_list, 10) 

    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'network/index.html', {'posts': posts})

def following(request):
    if request.user.is_authenticated:
        followed_users = Follow.objects.filter(user=request.user).values_list('profile_user', flat=True)
        posts_list = Posting.objects.filter(user__in=followed_users).order_by('-created_at')
    else:
        posts_list = Posting.objects.all().order_by('-created_at')

    paginator = Paginator(posts_list, 10) 

    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'network/following.html', {'posts': posts})

def update_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Posting, id=post_id)
        new_content = json.loads(request.body).get('content', '')
        if new_content:
            post.content = new_content
            post.save()
            return JsonResponse({'success': True, 'content': post.content})
        return JsonResponse({'success': False, 'error': 'No content provided'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

def like_post(request, post_id):
    try:
        post = Posting.objects.get(pk=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        likes_count = post.likes.count()
        return JsonResponse({'success': True, 'likes_count': likes_count, 'liked': liked})
    except Posting.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Post does not exist'}, status=404)

def toggle_follow(request, follow_id):
    if request.user.is_authenticated:
        profile_user = get_object_or_404(User, pk=follow_id)
        user = request.user

        on_follow = Follow.objects.filter(user=user, profile_user=profile_user).exists()
        if on_follow:
            Follow.objects.filter(user=user, profile_user=profile_user).delete()
        else:
            Follow.objects.create(user=user, profile_user=profile_user)

        return redirect('profile', user_id=follow_id)
    else:
        return HttpResponseRedirect(reverse('login'))

def profile(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    posts = Posting.objects.filter(user=profile_user).order_by('-created_at')

    if request.user.is_authenticated:
        follow = Follow.objects.filter(user=request.user)
        follow_users = [item.profile_user for item in follow]
    else:
        follow_users = []
    follower_count = profile_user.follower_count 
    following_count = profile_user.following_count 

    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'follow_users': follow_users,
        'follower_count': follower_count,
        'following_count': following_count
    })


def allP(request):
    posts_list = Posting.objects.all().order_by('-created_at')
    paginator = Paginator(posts_list, 10)

    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'network/allP.html', {'posts': posts})

def posting(request):
    if request.method == "POST":
        content = request.POST.get("content")
        
        if content:
            user = request.user 
            post = Posting(content=content, user=user)
            post.save()
            return HttpResponseRedirect(reverse('index'))  

  
    return HttpResponseRedirect(reverse('index'))  

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
