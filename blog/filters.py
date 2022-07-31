import django_filters
from django_filters import CharFilter
from .models import *

class PostFilter(django_filters.FilterSet):
    title= CharFilter(field_name='title', lookup_expr='icontains')
    class Meta:
        model = Post
        fields=['title','category','content','author','published_date']

class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model= Category
        fields='__all__'
