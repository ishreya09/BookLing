from django.db import models

# Create your models here.

from django.db import models

# Create your models here.
from product.models import Product

from account.models import Profile

class Wishlist(models.Model):
    customer= models.ForeignKey(Profile, on_delete=models.SET_NULL,null=True,blank=True)
    wishlist_id=models.BigAutoField(primary_key=True,serialize=False ,unique=True,auto_created=True )
    date_created= models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.wishlist_id)

    @property
    def get_wishlist_items(self):
        wishlistitems= self.wishlistitem_set.all()
        total= sum([item.quantity for item in wishlistitems])
        return total

class WishlistItem(models.Model):
    product= models.ForeignKey(Product, on_delete=models.SET_NULL,null=True,blank=True)
    wishlist= models.ForeignKey(Wishlist,on_delete=models.SET_NULL,null=True,blank=True)
    quantity= models.IntegerField(default=0,null=True,blank=True)
    date_added= models.DateTimeField(auto_now_add=True)