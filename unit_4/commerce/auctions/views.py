from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
import datetime


def index(request):
    items = Listing.objects.all().filter(avail=1)
    return render(request, "auctions/index.html", {
        'items': items
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def new(request):
    if request.method == "POST":
        print("post is successful")
        title = request.POST.get('title')
        description = request.POST.get('description')
        bid = float(request.POST.get('bid'))
        try:
            url = request.POST.get('url')
        except ValueError:
            url = "https://cdn4.iconfinder.com/data/icons/toolbar-std-pack/512/delete-256.png"
        #category
        avail = False
        owner = User.objects.get(pk=int(request.user.id))
        instance = Listing(title=title, description=description, bid=bid, url=url,\
             create_time=datetime.datetime.now(), avail=1, owner=owner)
        instance.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        cate = Category.objects.all()
        return render(request, "auctions/new.html", {
            "categories": cate
        })

def category(request):
    pass

def watchlist(request):
    pass

def listing(request, title):
    return render(request, "auctions/item.html", {
        'title': title
    })