from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.contrib.auth.models import auth

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    bio= models.CharField(max_length=500,null=True, blank= True)
    username=models.CharField(blank=True,null=True, max_length=200)
    email_confirmed = models.BooleanField(default=False)
    slug = models.SlugField(blank=True,null=True,auto_created=True)
    whatsapp_number = models.CharField(null=True, blank=True, max_length=15)
    whatsapplink=models.CharField(max_length=60,null=True,blank=True)
    SRN= models.CharField(max_length=100,blank=True,null=True)
    Campus=models.CharField(max_length=20,null=True,blank=True)
    Semester= models.CharField(max_length=100,null=True,blank=True)
    Course =models.CharField(max_length=100,null=True,blank=True,help_text="Eg. - BBA, B-tech,etc")
    review= models.IntegerField(default=0)
    def __str__(self):
        return self.slug

# class Address(models.Model):
#     #user = models.ForeignKey(User, on_delete= models.CASCADE)
#     profile= models.ForeignKey(Profile, on_delete= models.SET_NULL, null=True,blank=True)
#     #mobile_number= models.CharField(max_length=20, null= True)
#     address_1 =models.CharField(max_length=100,blank=True,null=True)
#     address_2 =models.CharField(max_length=100,blank=True,null=True)
#     landmark=models.CharField(max_length=100,blank=True,null=True)
#     pin_code=models.CharField(max_length=6,null=True,blank=True)
#     city= models.CharField(max_length=100,null=True,blank=True)
#     state =models.CharField(max_length=100,null=True,blank=True)
#     Country = models.CharField(max_length=40,null=True, blank=True,default="India")
#     date_added= models.DateTimeField(auto_now_add=True)