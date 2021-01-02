from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User,Userdetail,Post
import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def index(request):
    return render(request, "network/index.html")


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
# new_post/save_post to start

@login_required
def new_post(request):
    if request.method == "POST":
        form = Post(content=request.POST['content'])
        profileuser = Userdetail(user = request.user)
        # it checks if userdetail model exist request.user to provide first register user can post     
        if not Userdetail.objects.filter(user=request.user).exists():
            # print("user does not exist in Userdetail model, to be created")
            profileuser.save()
            # print("saved")
            form.creator = Userdetail.objects.get(user=request.user)
            # print(form.creator)
        else:
            # Profile.user.save()
            # print(Profile.user)
            form.creator = Userdetail.objects.get(user=request.user)
            # print(form.creator)
            # print("done")
        # print(form.creator)
        form.save()
    elif request.method == "PUT":
        # decode is neccessary later  python >= 3
        data = json.loads(request.body.decode('utf-8'))        
        # print(f"data: ${data}")
        post_id = int(data["post_id"])
        new_content = data["new_post"]
        post = Post.objects.filter(id=post_id).first()     
        if post.creator.user != request.user:
            return HttpResponse(status=401)
        post.content = new_content
        post.save()
        return JsonResponse({
            "result": True
        },status=200)
    else:
        return JsonResponse({
                "error": f"request methods supported: POST, GET"
            }, status=400)
    return index(request)
# getting datas
def load_posts(request):
    profile = request.GET.get("profile", None)
    if (profile):
        posts = Post.objects.filter(creator=profile).all()
    else:
        posts = Post.objects.all()
    # print(posts)
    return paginated_posts(request,posts)

def paginated_posts(request, posts):
    posts = posts.order_by("-created_date").all()
    paginator = Paginator(posts,10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return JsonResponse({
        "posts" : [post.serialize(request.user) for post in page_obj],
        "num_pages" : paginator.num_pages
    }, safe=False)

#  profile_pages/show_profile
def profile_page(request,user_id):
    profile = Userdetail.objects.filter(id=user_id).first()
    return JsonResponse(profile.serialize(request.user),status=200)

@login_required
def load_followed_posts(request):
     followed_profiles = request.user.get_followed_profiles.all()
    #  print(followed_profiles)
     posts = Post.objects.filter(creator__in = followed_profiles).all()
    #  print(f'posts: {posts}')
     return paginated_posts(request,posts)


def paginated_posts(request,posts):
    posts = posts.order_by("-created_date").all()  
    paginator = Paginator(posts,10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return JsonResponse({
        "posts": [post.serialize(request.user) for post in page_obj],
        "num_pages": paginator.num_pages
        }
        , safe=False)

# editing post is on JS, cos no routing on views.py
# For security, ensure that your application is designed 
# such that it is not possible for a user, via any route,
# to edit another user’s posts.


# counting like/update_like
@login_required
def count_like(request,post_id):
    # print("inside yes")
    user_profile = Userdetail.objects.filter(user=request.user).first()
    post = Post.objects.get(id=post_id)
    if post in user_profile.get_all_liked_posts.all():
        # print(post)
        like_status = False
        post.likes.remove(user_profile)
    else:
        like_status = True
        post.likes.add(user_profile)
    post.save()
    return JsonResponse({
        "liked": like_status,
        "count": post.likes.count()
    }, status = 200)


@login_required
def follow(request,user_id):
    user_profile = Userdetail.objects.get(id=user_id)
    if user_profile in request.user.get_followed_profiles.all():
        followable = False
        user_profile.followers.remove(request.user)
    else:
        followable = True
        user_profile.followers.add(request.user)
    user_profile.save()
    return JsonResponse({
        "followable":followable,
        "counter_follow": user_profile.followers.count()        
    },status=200)
