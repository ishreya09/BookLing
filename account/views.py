
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from account.tokens import account_activation_token
from django.core.mail import send_mail  
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import View

from product.models import Product
from .forms import ProfileForm

from django.contrib import messages
from django.shortcuts import render
from django.contrib import auth
from django.utils.text import slugify

from django.contrib.auth.models import User
from .models import Profile

from django.shortcuts import redirect

from django.contrib.auth.decorators import user_passes_test




# Create your views here.
def email_check(user):
    return user.email.endswith('@pesu.pes.edu')


def profile(request):
    user= request.user
    print(user)
    
    #profile = Profile.objects.all()
    #user=User.objects.all()
    context={'user':user,}#'profile':profile}
    return render(request,'account/profile.html',context)



def login(request):
    context={}
    return render(request,'account/login.html',context)

def login_submit(request):
    context={}
    if request.method == 'POST':
        print("hel")
        
        username = request.POST.get('username',False)
        password = request.POST.get('password',False)
        print(username,password)
        
        user = auth.authenticate(username=username, password= password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in successfully')
            return redirect('/')
        else:
            messages.error(request, 'invalid username or password')

            return redirect ('/account/login')
    else:
        pass


def sign_up(request):
    context={}
    return render(request,'account/signup.html',context)

def sign_up_submit(request):
    if request.method=='POST':
        
        #BASIC DETAILS
        firstname= request.POST.get('firstname',False)
        lastname= request.POST.get('lastname',False)
        username= request.POST.get('username',False)
        email= request.POST.get('email',False)
        whatsappno= request.POST.get('whatsappno',False)
        password1= request.POST.get('password1',False)
        password2= request.POST.get('password2',False)

        #Address Details
        SRN= request.POST.get('SRN',False)
        campus= request.POST.get('campus',False)
        sem=request.POST.get('sem',False)
        course= request.POST.get('course',False)
        
        
        #Personal Details
        #dob= request.POST.get('dob',False)
        bio= request.POST.get('bio',False)

        slug= slugify(username)
        print(slug)
        whatsapplink= "https://api.whatsapp.com/send?phone=91{}".format(whatsappno)
        print(whatsapplink)
        if password1 == password2:
            if User.objects.filter(username= username).exists():
                messages.info (request, "Username taken")
                return redirect('/account/sign_up')
            elif (User.objects.filter(email = email).exists()):
                messages.info (request, "Email already present")
                return redirect('/account/sign_up')
            else:
                user = User.objects.create_user(first_name= firstname, last_name= lastname ,username= username, password= password1, email= email )
                user.save()
                profile= Profile()
                profile.user=User.objects.get(username=username)
                profile.slug, profile.whatsapp_number,profile.whatsapplink, profile.bio=slug, whatsappno,whatsapplink,bio
                profile.SRN,profile.Campus,profile.Semester,profile.Course=SRN,campus,sem,course
                profile.username=username
                profile.save()
                
                messages.info (request, 'User Created')
                return redirect ('/account/login')
        else:
            messages.info (request, "password does not match")
            return redirect('/account/sign_up')
        return redirect ('/account/sign_up')

from blog.models import Post
      
@user_passes_test(email_check)
def profile_detail(request,slug=None):
    profile=Profile.objects.get(slug=slug)
    user=User.objects.get(username=profile.username)
    product=Product.objects.filter(user=user)
    posts=Post.objects.filter(user=user)
    context={'user':user,'product':product,'posts':posts}
    return render (request, 'account/profile_detail.html',context)



def confirm_email(request):
    user=request.user
    current_site = get_current_site(request)
    subject = 'Activate Your Bookling Account'
    message = render_to_string('account/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
    user.email_user(subject, message)

    messages.success(request, ('Your email confirmation is pending'))
    return redirect('/')


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            k=Profile.objects.get(user=user)
            k.email_confirmed=True
            k.save()
            user.save()
            auth.login(request, user)
            messages.success(request, ('Your email has been confirmed.'))
            return redirect('/')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('/')

        
        

def logout(request):
    auth.logout(request)
    messages.success(request,"You are logged out")
    return redirect('/')


def updateprofile(request):
    if request.method == 'POST':

        profile_form = ProfileForm(request.POST,request.FILES, instance=request.user.profile)
        
        if profile_form.is_valid():
            
            b= profile_form.save()
           
            profile= Profile.objects.get(user=request.user)
                       

            messages.success(request, 'Your profile is successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please provide valid details.')
            return redirect('/')
    else:
        
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'account/editprofile.html', {
        'profile_form': profile_form
        })

