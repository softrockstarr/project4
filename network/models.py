from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    content = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id} created by {self.user} on {self.date.strftime('%-I:%M:%S, %d %b, %Y')}"

class Follower(models.Model):
    user_following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followed")

    def __str__(self):
        return f"{self.user_following} is following {self.user_followed}"
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like")
    
    def __str__(self):
        return f"{self.user} liked {self.post}"


