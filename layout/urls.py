from django.urls import path
from . import views

urlpatterns= [
    path('', views.home,name= 'home'),
    path('about',views.about,name='about'),
    path('contact',views.contact_us,name="contact"),
    path('contact_success',views.contact_success,name="contact_success"),
    path('terms_and_condition',views.terms,name="terms_and_condition"),
]


