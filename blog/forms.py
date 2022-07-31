from blog.models import Category
from .models import Post
from django import forms
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    desc= forms.CharField(widget=CKEditorWidget())
    specification= forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = ('category', 
        'title',
        'metades',
        'image',
        'content',
        'author',
        'tags',)

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=(
            'name',
            'parent',
            'slug'
        )