from django.urls import path
from . import views

urlpatterns= [
    path('create_category',views.create_category, name="create_category"),
    path('create_product',views.create_product,name="create_product"),
    path('p/<slug:slug>', views.product_detail,name="product_detail"),
    path('c/<slug:slug>',views.category_detail,name="category_detail"),
    path('category_list',views.category_list,name="category_list"),
    path('',views.product_list,name='product_list'),
    
]