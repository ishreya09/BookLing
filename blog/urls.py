from django.urls import path
from django.conf.urls import include
from . import views

from django.conf.urls import url


app_name='blog'

urlpatterns = [
        url(r'^$',  views.post_list , name='post_list'),
        url(r'^(?P<slug>[\w-]+)/$', views.post_detail, name="detail"),
        url(r'^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
        path('tag/<slug:tag_slug>', views.post_list,name="posts_by_tag"),
        path('blog_create',views.create_blog,name="blog_create"),
        path('create_category',views.create_category,name="create_category")
    ]

