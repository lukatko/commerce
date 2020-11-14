from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Comment, Listing, Bid, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "Listings": Listing.objects.exclude(closed = 1)[::-1],
        "active": 1
    })

def closed_listings(request):
    return render(request, "auctions/index.html", {
        "Listings": Listing.objects.exclude(closed = 0)[::-1],
        "closed": 0
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

@login_required
def create(request):
    if request.method == "POST":
        author = request.user
        price = float(request.POST["price"])
        post_name = request.POST["name"]
        comment = Comment(comment = request.POST["comment"], image = request.POST["image"])
        comment.save()
        Listing(author = author, price = price, comment = comment, post_name=post_name, closed = 0).save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")

def listing(request, listing):
    listing = Listing.objects.get(pk = int(listing))
    try:
        if (hasattr(request.user, "watchlist")):
            request.user.watchlist
        else:
            watchlist = Watchlist(user = request.user)
            watchlist.save()
        watchlist = request.user.watchlist
        if (Bid.objects.filter(item = listing).count() > 0):
            is_winner = Bid.objects.get(amount = listing.price, item = listing).bidder == request.user
        else:
            is_winner = 0
        if request.method == "POST":
            price = float(request.POST["price"])
            if (price <= float(listing.price)):
                return render(request, "auctions/listing.html", {
                    "watchlist": watchlist.item.all(),
                    "listing": listing,
                    "flag": 1,
                    "is_author": request.user == listing.author,
                    "is_closed": listing.closed,
                    "is_winner": is_winner,
                    "bids": Bid.objects.filter(item = listing).count()
                })
            else:
                listing.price = price
                listing.save()
                Bid(bidder = request.user, item = listing, amount = price).save()
                return render(request, "auctions/listing.html", {
                    "watchlist": watchlist.item.all(),
                    "listing": listing,
                    "flag": 0,
                    "is_author": request.user == listing.author,
                    "is_closed": listing.closed,
                    "is_winner": is_winner,
                    "bids": Bid.objects.filter(item = listing).count()
                })
        else:
            return render(request, "auctions/listing.html", {
                "watchlist": watchlist.item.all(),
                "listing": listing,
                "flag": 0,
                "is_author": request.user == listing.author,
                "is_closed": listing.closed,
                "is_winner": is_winner,
                "bids": Bid.objects.filter(item = listing).count()
            })
    except:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "is_closed": listing.closed
        })

def closed(request, listing):
    listing = Listing.objects.get(pk = int(listing))
    listing.closed = 1
    listing.save()
    return HttpResponseRedirect(reverse("listing", args = (listing.id, )))

@login_required
def add_to_watchlist(request, listing):
    users_watchlist = request.user.watchlist
    users_watchlist.item.add(Listing.objects.get(pk = int(listing)))
    return HttpResponseRedirect(reverse("listing", args = (listing, )))

@login_required
def remove_from_watchlist(request, listing):
    users_watchlist = request.user.watchlist
    users_watchlist.item.remove(Listing.objects.get(pk = int(listing)))
    return HttpResponseRedirect(reverse("listing", args = (listing, )))

@login_required
def watchlist(request):
    try:
        request.user.watchlist
    except:
        watchlist = Watchlist(user = request.user)
        watchlist.save()
    watchlist = request.user.watchlist
    for listing in watchlist.item.all():
        if (listing.closed):
            watchlist.item.remove(listing)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist.item.all()
    })





