from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Comment(models.Model):
    comment = models.TextField()
    image = models.CharField(max_length=100)

class Listing(models.Model):
    post_name = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    price = models.FloatField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.post_name}"
    

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete = models.CASCADE, related_name="user_bids")
    item = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name="listing_bids")