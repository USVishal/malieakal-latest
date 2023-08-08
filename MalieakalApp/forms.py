from django import forms
from .models import User_Registration
from django.core.exceptions import ValidationError
import re
from django.core.validators import EmailValidator
from django.contrib import messages

from django.core.validators import RegexValidator

########################################################<<<<<<<<< Creator Userform >>>>>>>>>>>>>>>>>

class User_RegistrationForm(forms.ModelForm):

        gender = forms.ChoiceField(choices=[
            ('Gender', 'Gender'),
            ('Female', 'Female'),
            ('Male', 'Male'),
            ('Other', 'Other'),
        ], widget=forms.Select(attrs={'class': 'form-control item', 'id': 'Gender', 'placeholder': 'Gender'}))
        
        # profession = forms.ChoiceField(choices=[
        #     ('Profession', 'Profession'),
        #     ('Actor', 'Actor'),
        #     ('Costume_Designer', 'Costume_Designer'),
            
        # ], widget=forms.Select(attrs={'class': 'form-control item', 'id': 'profession', 'placeholder': 'Profession'}))
        
        date_of_birth = forms.DateField(
             widget=forms.DateInput(attrs={'class': 'form-control item', 
                                           'id': 'birthday', 'placeholder': 'Date of Birth',
                                           'type': 'date',}))

        class Meta:
            model = User_Registration
            fields = '__all__'
        
            widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control item','placeholder':'Firstname'}),
                'lastname': forms.TextInput(attrs={'class': 'form-control item','placeholder':'Lastname'}),
                'nickname': forms.TextInput(attrs={'class': 'form-control item','placeholder':'Nickname'}),
                'phone_number': forms.TextInput(attrs={'class': 'form-control item','placeholder':'Phone number','pattern': "^(0|\+91)?(?!6789)[6-9]\d{9}$",
    'message': "Enter a valid phone number"}),
 

                'email': forms.EmailInput(attrs={'class': 'form-control item','placeholder':'Email','id':'email','pattern':"[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$"}),
                # 'experience': forms.NumberInput(attrs={'class': 'form-control item','placeholder':'Experience'}),
                'role': forms.HiddenInput(attrs={'value': 'PREFIX_VALUE','id': 'role-field'}),
                # 'profileimage' : forms.FileField()

                }
            
          
            
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['username'].required = False
            self.fields['password'].required = False




class ImageForm(forms.Form):
    image_1 = forms.ImageField(label='Banner 1(resolution W-1600px H-529px)')
    label_1 = forms.CharField(label='Banner Title 1', max_length=100)

    image_2 = forms.ImageField(label='Banner 2(resolution W-1600px H-529px)')
    label_2 = forms.CharField(label='Banner Title 2', max_length=100)

    image_3 = forms.ImageField(label='Banner 3(resolution W-1600px H-529px)')
    label_3 = forms.CharField(label='Banner Title 3', max_length=100)

    image_4 = forms.ImageField(label='Banner 4(resolution W-1600px H-529px)')
    label_4 = forms.CharField(label='Banner Title 4', max_length=100)

    image_5 = forms.ImageField(label='Banner 5(resolution W-1600px H-529px)')
    label_5 = forms.CharField(label='Banner Title 5', max_length=100)


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User_Registration
        fields = '__all__'
