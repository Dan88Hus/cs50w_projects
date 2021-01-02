
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("load_posts", views.load_posts, name="load_posts"),
    path("profile_page/<int:user_id>",views.profile_page,name="profile_page"),
    path("load_posts/followed",views.load_followed_posts,name="load_followed_posts"),
    path("post/<int:post_id>/count_like",views.count_like, name="count_like"),
    path("profile_page/<int:user_id>/follow",views.follow,name="follow"),




    
]
