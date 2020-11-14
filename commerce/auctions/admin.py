from django.contrib import admin

from .models import User, Comment, Listing, Bid, Watchlist

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Watchlist)