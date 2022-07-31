import json
from .models import *
from account.models import *
from product.models import *

def cookieWishlist(request):
    try:
        wish= json.loads(request.COOKIES['wish'])
    except:
        wish={}
    print ('wish:', wish)
    items=[]
    wishlist={'get_wishlist_items':0}
    wishItems=wishlist['get_wishlist_items']

    for i in wish:
        try:
            wishItems += int(wish[i]['quantity'])
            product= Product.objects.get(product_id=i)
            wishlist['get_wishlist_items'] += int(wish[i]['quantity'])

            item={
                'product':{
                    'product_id': product.product_id,
                    'product_name': product.product_name,
                    'imageURL' : product.imageURL,
                    'price':product.price,
                    'product_slug': product.product_slug,


                    },
                'quantity': int(wish[i]['quantity']),

                    }
            items.append(item)
        except:
            pass

            
    return {'items':items, 'wishlist':wishlist,'wishItems':wishItems}

def wishlistData(request):
    if request.user.is_authenticated:
        customer= request.user.profile
        wishlist, created= Wishlist.objects.get_or_create(customer=customer)
        items= wishlist.wishlistitem_set.all()
        wishItems= wishlist.get_wishlist_items
    else:
        cookieWish= cookieWishlist(request)
        wishItems= cookieWish['wishItems']
        wishlist= cookieWish['wishlist']
        items= cookieWish['items']
    return {'items':items, 'wishlist':wishlist,'wishItems':wishItems}
