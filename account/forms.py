from .models import Profile
from django import forms

class ProfileForm(forms.ModelForm):
    whatsapp_number=forms.CharField(required= True, help_text ="Enter your whatsapp number without your country code")
    class Meta:
        model = Profile
        fields = ('bio', 
        'whatsapp_number',
        'SRN',
        'Campus',
        'Course',
        'Semester',)