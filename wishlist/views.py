from wishlist.utils import cookieWishlist, wishlistData

from django.shortcuts import render

from product.models import Product,Category
from .models import *
# Create your views here.
from django.http import JsonResponse
import json

def wishlist(request):

    WData= wishlistData(request)
    wishItems = WData['wishItems']
    items= WData['items']
    wishlist=WData['wishlist']

    context={'items':items,'wishlist':wishlist,'wishItems':wishItems}
    return render(request, 'wishlist/wishlist.html',context)

def add_item(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    
    print('Action:',action,' product id:', productId)

    customer=request.user.profile
    product= Product.objects.get(product_id= productId)
    wishlist, created= Wishlist.objects.get_or_create(customer=customer)

    wishlistItem,created= WishlistItem.objects.get_or_create(wishlist=wishlist,product=product)

    
    if action == 'addtowishlist':
        wishlistItem.quantity=1
        
    
    elif action=='remove':
        wishlistItem.quantity=0
        print(wishlistItem)
    
        
    wishlistItem.save()


    product.save()

    if wishlistItem.quantity == 0:
        wishlistItem.delete()
    

    return JsonResponse('Item was added', safe=False)

# from django.shortcuts import render
# from product.models import Product,Category
# from .models import *

# def add_items(request):
