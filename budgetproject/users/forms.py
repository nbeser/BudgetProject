from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'E-mail'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Şifre'
        })
    )

    labels = {
        "username": "E-mail",
        "password": "Parola"
    }


class UserSignupForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parola'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parola Tekrar', 
        })
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "password1", "password2", "first_name", "last_name")
        widgets = {
            "email": forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            "first_name": forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'İsim'}),
            "last_name": forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Soy İsim'}),
        }
        labels = {
            "email": "E-Mail",
            "password1": "Parola",
            "password2": "Parola Tekrar",
            "first_name": "İsim",
            "last_name": "Soy İsim"
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].label = "Parola"
        self.fields['password2'].label = "Parola Tekrar"

