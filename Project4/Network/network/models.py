from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Userdetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name="get_followed_profiles")

    def serialize(self,user):
        return {
            "userdetail_id": self.user.id,
            "userdetail_username": self.user.username,
            "userdetail_followers": self.followers.count(),
            "userdetail_following": self.user.get_followed_profiles.count(),
            "userdetail_currently_following": not user.is_anonymous and self in user.get_followed_profiles.all(),
            "userdetail_follow_available": (not user.is_anonymous) and self.user != user
        }
    def __str__(self):
        userdetail_followers_str = ""
        for follower in self.followers.all():
            userdetail_followers_str+= " " + follower.username
        return f"id: {self.user.id},{self.user.username}; followed by {userdetail_followers_str}"

class Post(models.Model):
    content = models.CharField(max_length=140)
    created_date = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(Userdetail, on_delete=models.CASCADE, related_name="get_all_posts")
    likes = models.ManyToManyField(Userdetail, blank=True, related_name="get_all_liked_posts")

    def serialize(self, user):
        return {
            "post_id": self.id,
            "post_content": self.content,
            "post_created_date": self.created_date.strftime("%b %#d %Y, %#I:%M"),
            "post_creator_id": self.creator.id,
            "post_creator_username": self.creator.user.username,
            "post_likes": self.likes.count(),
            "post_liked": not user.is_anonymous and self in Userdetail.objects.filter(user=user).first().get_all_liked_posts.all(),
            "post_editable": self.creator.user == user
        }
    def __str__(self):
        return f"Creator: {self.creator}, Created date: {self.created_date}"