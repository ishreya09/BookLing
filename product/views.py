from django.shortcuts import render
from django.shortcuts import redirect

from .forms import ProductForm
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib import messages

from .models import Category,Product

# Create your views here.
from django.contrib.auth.decorators import user_passes_test

def email_check(user):
    return user.email.endswith('@pesu.pes.edu')
    

@user_passes_test(email_check)
def create_product(request):
    if request.method=='POST':
        if product_form.is_valid():
            p= product_form.save()
            p= Product.objects.get(id=p.id)
            p.product_slug= p.id
            p.user=request.user
            p.save()
            messages.info("Product is added!!")
            return redirect('/')
        messages.error("Product not added")
        return redirect('/')
        
    elif request.method=='GET':
        product_form = ProductForm(instance=request.user)
        context={'product_form':product_form}
        return render(request,'product/product_create.html',context)


def validate_digits_letters(username):
    for char in username:
        if not char.isdigit() or not char.isalpha() or char!="_":
            return False
    return True

@user_passes_test(email_check)
def product_list(request):
    p=Product.objects.all()
    context={'product':p}
    return render(request,'product/product_list.html',context)


@user_passes_test(email_check)
def product_detail(request,slug=None):
    p=Product.objects.filter(product_slug=slug)
    context={'product':p[0]}
    
    return render(request,'product/product_detail.html',context)

@user_passes_test(email_check)
def category_list(request):
    c=Category.objects.all()
    context={'category':c}
    return render(request,'product/category_list.html',context)

@user_passes_test(email_check)
def category_detail(request,slug=None):
    c=Category.objects.filter(category_slug=slug)
    p=Product.objects.filter(category=c)
    context={'product':p,'category':c}
    return render(request, 'product/category_detail.html',context)




@staff_member_required
@user_passes_test(email_check)
def create_category(request):
    context={}
    if request.method=='POST':
        categoryname=request.POST.get('categoryname', False)
        slug="-".join(categoryname.split())
        c=Category()
        c.name,c.category_slug= categoryname,slug
        c.save()
        print(slug)

        return redirect('product/create_category')
    return render(request,'product/category_create.html',context)



