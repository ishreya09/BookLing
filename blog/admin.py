from django.contrib import admin

# Register your models here.

from .models import Post
from .models import Category
from mptt.admin import MPTTModelAdmin

class PostAdmin(admin.ModelAdmin):
    list_display=('title','category','slug','author')
    search_fields=[
        'title',
        'category',
        'slug',
        'metades',
        'content',
        'image',
        'author',
    ]
    list_filter=[
        'category'
    ]
    list_editable=['category',]


admin.site.register(Post,PostAdmin)
admin.site.register(Category , MPTTModelAdmin) 