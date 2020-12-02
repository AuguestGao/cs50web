from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, max_length=1000)
    bid = models.DecimalField(max_digits=20, decimal_places=2)
    url = models.URLField(blank=True, max_length = 255)
    category = models.ForeignKey(Category, null=True, related_name="item", on_delete=models.SET_NULL)
    create_time = models.DateTimeField()
    avail = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")

    def __str__(self):
        return self.title