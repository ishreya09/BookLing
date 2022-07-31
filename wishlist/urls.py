from django.urls import path

from . import views

urlpatterns= [
    path('',views.wishlist, name="wishlist"),
    path('add_item', views.add_item ,name= "add_item"),
]