from django import forms
from .models import Photos, CreatePartyRoom
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()


class UploadPhotoForm(forms.ModelForm):
    class Meta:
        model = Photos
        fields = ['photo_room_image']

class CreatePartyRoomForm(forms.ModelForm):
    class Meta:
        model = CreatePartyRoom
        fields = ['name','date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'width': '200px'
                }),
                'date': forms.TextInput(attrs={
                'class': 'form-control',
                'width': '200'
                }),
        }


class RegistrationForm(UserCreationForm):
    #captcha = ReCaptchaField()
    password1 = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'password',
        'placeholder': 'Password'
    }))
    password2 = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'password',
        'placeholder': 'Repeat Password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email':    forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            })

        }


    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user
