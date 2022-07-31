from django.urls import path
from . import views

from django.contrib.auth import views as auth_views
from .views import ActivateAccount

urlpatterns= [
    path('profile', views.profile,name= 'profile'),
    path('login',views.login,name="login"),
    path('login_success',views.login_submit,name="login_success"),
    path('sign_up',views.sign_up,name="sign_up"),
    path('logout',views.logout,name="logout"),
    path('sign_confirm',views.sign_up_submit,name="sign_confirm"),
    path('email_confirm',views.confirm_email,name="email_confirm"),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),

    path('saveprofile/', views.updateprofile , name= "saveprofile"),
    path('updateprofile/', views.updateprofile , name= 'updateprofile'),

    path('profile/<slug:slug>',views.profile_detail,name="profile_detail"),    
    # Change Password
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='account/change-password.html',
            success_url = '/') ,  name='change_password'),
    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='account/password-reset.html',
             subject_template_name='account/password_reset_subject.txt',
             email_template_name='account/password_reset_email.html',
            #  success_url='login'
         ),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password-reset-done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
