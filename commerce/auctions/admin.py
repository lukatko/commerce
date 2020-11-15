from django.contrib import admin

from .models import User, Comment, Listing, Bid, Watchlist, Comment_under_post, Category

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Watchlist)
admin.site.register(Comment_under_post)
admin.site.register(Category)