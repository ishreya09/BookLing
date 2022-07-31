from django.db import models

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

# Create your models here.
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
class Category(models.Model):
    category_id= models.BigAutoField(primary_key=True, auto_created=True)
    category_slug = models.SlugField(max_length=200, db_index=True, unique=True, auto_created=True)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Product(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    category =models.ForeignKey(Category,on_delete=models.CASCADE)
    product_id = models.BigAutoField(primary_key=True, auto_created=True)
    product_slug = models.SlugField(max_length=200, db_index=True, unique=True, auto_created=True)
    name = models.CharField(max_length=500)
    author =models.CharField(max_length=500,blank=True,null=True)
    desc =  RichTextField()
    specification = RichTextUploadingField(null=True,blank=True)
    product_cover_image = models.ImageField(upload_to='products_img',verbose_name= "Cover Image")
    image1=models.ImageField(upload_to='products_img',null=True,blank=True, verbose_name="2nd Image")
    image2=models.ImageField(upload_to='products_img',null=True,blank=True, verbose_name="3rd Image")
    image3=models.ImageField(upload_to='products_img',null=True,blank=True, verbose_name="4th Image")
    image4=models.ImageField(upload_to='products_img',null=True,blank=True, verbose_name="5th Image")
    price = models.DecimalField(help_text="MRP",max_digits=9, decimal_places=2)
    featured_product = models.BooleanField(default=False)
    tags=TaggableManager()
    sold=models.BooleanField(default=False)
    date_added= models.DateTimeField(auto_now_add=True)
    
    
