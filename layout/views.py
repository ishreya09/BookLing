from django.shortcuts import render

from layout.models import ContactUs, HomeImage

# Create your views here.

def home(request):
    img= HomeImage.objects.all()
    context={'img':img}
    return render(request, 'layout/home.html', context)

def about(request):
    context={}
    return render(request, 'layout/about.html', context)
    
def contact_us(request):
    context={}
    
    return render(request, 'layout/contact.html', context)
    
def contact_success(request):
    context={}
    if request.method=='POST':
        contact=ContactUs()
        name= request.POST.get('name',False)
        email=request.POST.get('email',False)
        subject= request.POST.get('subject',False)
        message= request.POST.get('message',False)
        contact.name, contact.email, contact.subject , contact.text= name, email,subject, message
        contact.save()
        context={'contact':contact}
    return render(request, 'layout/contact_success.html', context)


def terms(request): 
    context={}   
    return render(request, 'layout/terms.html', context)





