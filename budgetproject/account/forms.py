from django import forms
from django.contrib.auth import get_user_model
from .models import Account


User = get_user_model()


class CreateAccount(forms.ModelForm):
    opening_balance = forms.DecimalField(
        required=False,
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Açılış Miktarı'
        })
    )
    
    class Meta:
        model = Account
        fields = ("name", "account_type", "currency", "is_active")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "account_type": forms.Select(attrs={"class": "form-control"}),
            "currency": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(),
        }

        labels = {
            "name": "Hesap Adı",
            "account_type": "Hesap Tipi",
            "currency": "Birim",
            "is_active": "Aktif mi?"
        }
    
    def save(self, commit=True):
        opening_balance_value = self.cleaned_data.get('opening_balance')
        self.instance._opening_balance = opening_balance_value
        return super().save(commit=commit)



class UpdateAccount(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("name", "account_type", "currency", "is_active")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "account_type": forms.Select(attrs={"class": "form-control"}),
            "currency": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(),
        }
    
        labels = {
            "name": "Hesap Adı",
            "account_type": "Hesap Tipi",
            "currency": "Birim",
            "is_active": "Aktif mi?"
        }