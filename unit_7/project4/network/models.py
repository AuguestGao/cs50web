from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="owner")
    content = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User)

    class Meta:
        ordering = ["-timestamp"]

    def serialize(self):
        return {
            "id": self.id,
            "owner": self.by.id,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%Y-%m-%d, %I:%m %p"),
            "liked": self.liked,
        }


class Follow(models.Model):
    follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follow")
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )