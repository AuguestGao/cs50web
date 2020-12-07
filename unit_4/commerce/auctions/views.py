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

def cate_index(request):
    types = list(Category.objects.all())
    return render(request, "auctions/cate_index.html", {
        'types': types 
    })

def cate_name(request, name):
    cate_id = Category.objects.get(name=name)
    items = list(Listing.objects.filter(category = cate_id))
    return render(request, "auctions/cate_name.html", {
        "items": items,
        "name": name
    })

def watchlist(request):
     # user must login to see this page, so this step ensures the user existed and logged in already
    watch_who = User.objects.get(pk=request.user.id)
    
    if request.method == "POST":
        watch_item = Listing.objects.get(pk=int(request.POST.get('item_id')))

        if int(request.POST.get('found')):
            instance = Watchlist.objects.get(who=watch_who, item=watch_item)
            instance.delete()
        else:
            instance = Watchlist(who = watch_who) #create an Watchlist object
            instance.save() # save instance first and then relate to the Listing object
            instance.item.add(watch_item)

    watched_items = list(Watchlist.objects.filter(who=watch_who).values_list('item', flat=True)) #use values_list with flat to get the item.id only instead of a dictionary 
    items = Listing.objects.filter(pk__in= watched_items) #get listing objects by index, pk__in takes id in int format
    return render(request, "auctions/watchlist.html", {
        "items": items,
    })

def item(request, id):
    item = Listing.objects.get(pk = id)
    user = User.objects.get(pk=request.user.id)
    exist = Watchlist.objects.filter(who=request.user.id, item=item.id).count()

    #save comment into db
    if request.method == 'POST':
        detail = request.POST.get('detail')
        instance = Comment(item = item, user=user, detail=detail, time=datetime.datetime.now())
        instance.save()

    comments = list(Comment.objects.filter(item=item))

    return render(request, "auctions/item.html", {
        'item': item,
        'exist': exist,
        'comments': comments
    })