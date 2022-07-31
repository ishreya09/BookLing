from django.contrib import admin

from .models import ContactUs,HomeImage
# Register your models here.

class HomeImageAdmin(admin.ModelAdmin):
    list_display=('image','active')
    list_filter=[
        'active'
    ]
    list_editable=['active',]

class ContactUsAdmin(admin.ModelAdmin):
    list_display= ('name','email','subject','sent_on')
    search_field=[
        'email',
        'sent_on',
    ]

admin.site.register(HomeImage,HomeImageAdmin)
admin.site.register(ContactUs,ContactUsAdmin)
