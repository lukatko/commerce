from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name = "create"),
    path("listing/<int:listing>", views.listing, name = "listing"),
    path("add_to_watchlist/<int:listing>", views.add_to_watchlist, name = "add_watchlist"),
    path("remove_from_watchlist/<int:listing>", views.remove_from_watchlist, name = "remove_watchlist"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("close/<int:listing>", views.closed, name = "close"),
    path("closed", views.closed_listings, name = "closed"),
    path("add_comment/<int:listing>", views.add_comment, name = "add_comment"),
    path("categories", views.categories, name = "categories"),
    path("category/<slug:slug>", views.category, name = "category")
]
