from django import forms

from ckeditor.widgets import CKEditorWidget
from .models import Product,Category

class ProductForm(forms.ModelForm):
    desc= forms.CharField(widget=CKEditorWidget())
    specification= forms.CharField(widget=CKEditorWidget())
    featured_product= forms.BooleanField()
    sold= forms.BooleanField()

    class Meta:
        model = Product
        fields = ('category', 
        'name',
        'author',
        'product_cover_image',
        'image1',
        'image2',
        'image3',
        'image4',
        'price',
        'tags',
        )

