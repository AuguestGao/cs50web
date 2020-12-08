from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
import datetime


def index(request):
    # current_winner = Bid.objects.filter(item=item).latest().user

    try:
        user=User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        pass
    else:
        # check if this user has a wining bid
        closing_items = list(Listing.objects.filter(avail=2))
        for item in closing_items:
            win = Bid.objects.filter(item=item).latest()
            if user.id == win.user.id:
                item.avail = 0
                item.save()
                message = "Congratulations! You have won " + str(item.title)
                return render(request, "auctions/deal.html", {
                    'item': item,
                    'message': message,
                    'price': win.price
                })

    key = "index"
    items = make_list(key)
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
        title = request.POST.get('title')
        description = request.POST.get('description')
        bid = float(request.POST.get('bid'))
        now = datetime.datetime.now()
        try:
            url = request.POST.get('url')
        except ValueError:
            url = "https://cdn4.iconfinder.com/data/icons/toolbar-std-pack/512/delete-256.png"
        
        avail = False
        owner = User.objects.get(pk=int(request.user.id))
        lst_instance = Listing(title=title, description=description, url=url,\
             create_time=now, avail=1, owner=owner)
        lst_instance.save()
        bid_instance = Bid(user = owner, item = lst_instance, price=bid, time=now)
        bid_instance.save()
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
    # items = list(Listing.objects.filter(category = cate_id))
    key = "cate"
    items = make_list(key, cate_id=cate_id)

    return render(request, "auctions/cate_name.html", {
        "items": items,
        "name": name
    })

def watchlist(request):
     # user must login to see this page, so this step ensures the user existed and logged in already
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        message = "Please login"
        return HttpResponseRedirect(reverse("login", args=(message,)))
    
    if request.method == "POST":
        item = Listing.objects.get(pk=int(request.POST.get('item_id')))

        if int(request.POST.get('found')):
            instance = Watchlist.objects.get(who=user, item=item)
            instance.delete()
        else:
            instance = Watchlist(who = user) #create an Watchlist object
            instance.save() # save instance first and then relate to the Listing object
            instance.item.add(item)

    # watched_items = list(Watchlist.objects.filter(who=watch_who).values_list('item', flat=True)) #use values_list with flat to get the item.id only instead of a dictionary 
    # items = Listing.objects.filter(pk__in= watched_items) #get listing objects by index, pk__in takes id in int format
    key = "watch"
    items = make_list(key, user=user)

    return render(request, "auctions/watchlist.html", {
        "items": items,
    })

def item(request, id):
    item = Listing.objects.get(pk = id)
    now=datetime.datetime.now()
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None
        exist = 0
    else:
        exist = Watchlist.objects.filter(who=user, item=item)

    #save comment into db
    if request.method == 'POST':
        # check if the user logged in yet
        if not user:
            message = "Please login"
            return HttpResponseRedirect(reverse("login", args=(message,)))

        if request.POST.get('close'):
            item.avail = 2
            item.save()
            current_price = Bid.objects.filter(item=item).latest().price
            message = str(item.title) + " is now closed."
            print(message)
            return render(request, "auctions/deal.html", {
                'message': message,
                'item': item,
                'price': current_price
            })

        # check if it's a comment
        if request.POST.get('detail'):
            detail = request.POST.get('detail')
            instance = Comment(item = item, user=user, detail=detail, time=now)
            instance.save()

        # check if it's a bid
        if request.POST.get('bid'):
            price = request.POST.get('bid')
            instance = Bid(user=user, item=item, price=price, time=now)
            instance.save()
    
    current_price = Bid.objects.filter(item=item).latest().price
    comments = list(Comment.objects.filter(item=item))

    return render(request, "auctions/item.html", {
        'item': item,
        'exist': exist,
        'comments': comments,
        'price': current_price,
        'owner': item.owner.id == user.id
    })

def make_list(key, cate_id=0, user=None):
    """get user, category and return a list which fulfill the request

    Args:
        user ([User]): get current logged in user info, or None type, i.e. not logged in
        cate_id ([int], optional): category filter. Defaults to 0.
        watchlist ([Boolean], optional): watchlist filter. Defaults to False.

    """
    show_list = {}

    #for cate_name.html
    if key == 'cate':
        items = list(Listing.objects.filter(category = cate_id))
    
    #for watchlist.html
    elif key == 'watch':
        watched_items = list(Watchlist.objects.filter(who=user).values_list('item', flat=True)) #use values_list with flat to get the item.id only instead of a dictionary 
        items =Listing.objects.filter(pk__in= watched_items) #get listing objects by index, pk__in takes id in int format

    #for index.html
    elif key == 'index': 
        items = Listing.objects.all().filter(avail=1)
    
    # wrap bid in
    for item in items:
        price = Bid.objects.filter(item=item).latest().price #get max price for each item
        show_list[item] = price
    
    return show_list
