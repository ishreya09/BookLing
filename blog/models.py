from django.db import models

# Create your models here.
from django.db import models
import django.utils.timezone 

from mptt.models import MPTTModel, TreeForeignKey
from mptt.models import TreeManyToManyField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

from django.contrib.auth.models import User




from django.utils import timezone
from django.db.models import Q

class PostQuerySet(models.QuerySet):
  def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(title__icontains=query) | 
                         Q(content__icontains=query)|
                         Q(slug__icontains=query)|
                         Q(category__name__icontains=query)|
                         Q(author__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs




class PostManager(models.Manager):
  def get_queryset(self):
    return PostQuerySet(self.model,using= self._db)
  
  def search(self, query=None):
    return self.get_queryset().search(query=query)
    


class Post(models.Model):
  user=  models.ForeignKey(User,on_delete=models.CASCADE)
  id= models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
  title = models.CharField(max_length=500)
  category = TreeForeignKey('Category',null=True,blank=True,on_delete= models.CASCADE, default="uncategorised")
  slug = models.SlugField(unique=True)
  metades= models.CharField(max_length=1000, help_text="for extra description before the content")
  image=models.ImageField(upload_to='blog_img',blank=True,null=True,verbose_name="Featured Image")
  content= RichTextUploadingField(blank=True,null=True)
  #content = models.TextField('Content', help_text="html content can be used for styling and different purposes",default="null")
  author= models.CharField(max_length=500,default="anonymous")
  published_date= models.DateField(auto_now_add=True,blank=True,null=True)
  tags=TaggableManager()
  objects= PostManager()


  def get_slug_list_for_categories(self):
      try:
          ancestors = self.category.get_ancestors(include_self=True)
      except:
          ancestors = []
      else:
          ancestors = [ i.slug for i in ancestors]
      slugs = []

      for i in range(len(ancestors)):
          slugs.append('/'.join(ancestors[:i+1]))
      return slugs
  def __str__(self):
      return self.title


class CategoryQuerySet(models.QuerySet):
  def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(name__icontains=query) |
                         Q(slug__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs




class CategoryManager(models.Manager):
  def get_queryset(self):
    return CategoryQuerySet(self.model,using= self._db)
  
  def search(self, query=None):
    return self.get_queryset().search(query=query)

  def get_ancestors(self,qs):
    tree_list = {}
    query = Q()
    for node in qs:
        if node.tree_id not in tree_list:
            tree_list[node.tree_id] = []

        parent =  node.parent.pk if node.parent is not None else None,

        if parent not in tree_list[node.tree_id]:
            tree_list[node.tree_id].append(parent)

            query |= Q(lft__lt=node.lft, rght__gt=node.rght, tree_id=node.tree_id)

    return Category.objects.filter(query)
    




class Category(MPTTModel):
  id= models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
  name = models.CharField(max_length=50, unique=True)
  parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,on_delete= models.CASCADE, default="parent")
  slug = models.SlugField(unique=True)
  objects= CategoryManager()

  class MPTTMeta:
    order_insertion_by = ['name']

  class Meta:
    unique_together = (('parent', 'slug',))
    verbose_name_plural = 'categories'

  def get_slug_list(self):
    try:
      ancestors = self.get_ancestors(include_self=True)
    except:
      ancestors = []
    else:
      ancestors = [ i.slug for i in ancestors]
    slugs = []
    for i in range(len(ancestors)):
      slugs.append('/'.join(ancestors[:i+1]))
    return slugs

  def __str__(self):
    return self.name