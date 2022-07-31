from django.db import models

# Create your models here.
from django.utils import timezone

class HomeImage(models.Model):
    image =models.ImageField(upload_to= 'layout_pics', help_text= 'try to add .png or .jpg files for easier accomoadation of images',null=True,blank=True)
    active= models.BooleanField(default= False, help_text="to make it as an active set of images")

class ContactUs(models.Model):
    name= models.CharField(max_length=300,null=True,blank=True)
    email=models.EmailField()
    subject=models.CharField(max_length=2000,default="No Subject")
    text=models.TextField()
    sent_on= models.DateTimeField(default=timezone.now)