
from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
from django.shortcuts import render , get_object_or_404
from blog.models import Post 
from blog.models import Category
from taggit.models import Tag
from django.db.models import Count
from .filters import PostFilter
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage


from django.contrib.auth.decorators import user_passes_test

def email_check(user):
    return user.email.endswith('@pesu.pes.edu')
    

@user_passes_test(email_check)
def show_category(request,hierarchy= None):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()
    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug = slug)

    try:
        instance = Category.objects.get(parent=parent,slug=category_slug[-1])
        
            
    except:
        instance = get_object_or_404(Post, slug = category_slug[-1])
        return render(request, "blog/post_detail.html", {'instance':instance,})
    else:
        context={'instance':instance}
        return render(request, 'blog/category.html', context)

@user_passes_test(email_check)
def post_detail(request,slug=None,tag_slug=None):
    instance = get_object_or_404(Post,slug=slug)

    post_tag_id= Post.tags.values_list('id',flat= True)
    similar_post= Post.objects.filter(tags__in= post_tag_id).exclude(id=instance.id)
    similar_post= similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags','-published_date')[:6]

    tag=None
    if tag_slug:
        tag= get_object_or_404(Tag,slug=tag_slug)
        
    context={'instance': instance , 'similar_post': similar_post,'tag':tag}
    return render(request,"blog/post_detail.html", context)

@user_passes_test(email_check)
def post_list(request,slug=None,tag_slug=None):
    posts = Post.objects.all()

    p = Paginator(posts, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    
    try:
        category1=Category.objects.get_ancestors(Category.objects.all())
    except:
        category1= Category.objects.none()

    tag=None
    if tag_slug:
        tag= get_object_or_404(Tag,slug=tag_slug)
        posts=Post.objects.filter(tags__in=[tag]) 
        p = Paginator(posts, 5)

        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = p.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = p.page(p.num_pages)

    context={ 'posts':posts,'category':category1,'page_obj':page_obj,'tag':tag}
    return render(request,"blog/post_list.html",context)

from .forms import PostForm,CategoryForm
from django.contrib import messages
from django.shortcuts import redirect

@user_passes_test(email_check)
def create_blog(request):
    if request.method=="POST":
        if post_form.is_valid():
            p= post_form.save()
            p= Post.objects.get(id=p.id)
            p.slug= p.id
            p.user=request.user
            p.save()
            messages.info("Blog Post is added!!")
            return redirect('/')
        messages.error("Blog Post is not added")
        return redirect('/')
        
    elif request.method=='GET':
        post_form = PostForm(instance=request.user)
        context={'post_form':post_form}
        return render(request,'blog/blog_create.html',context)


from django.contrib.admin.views.decorators import staff_member_required

@user_passes_test
@staff_member_required
def create_category(request):
    if request.method=="POST":
        if category_form.is_valid():
            p= category_form.save()
            p= Category.objects.get(id=p.id)            
            p.save()
            messages.info("Blog Post is added!!")
            return redirect('/')
        messages.error("Blog Post is not added")
        return redirect('/')
        
    elif request.method=='GET':
        category_form = CategoryForm(instance=request.user)
        context={'post_form':category_form}
        return render(request,'blog/category_create.html',context)


