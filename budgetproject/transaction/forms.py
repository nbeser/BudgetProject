from django import forms
from django.contrib.auth import get_user_model
from .models import Transaction

from account.models import Account
from category.models import Category


User = get_user_model()



class CreateTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ("account", "category", "amount", "description")
        widgets = {
            "account": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0,00"}),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Hatırlatıcı not..."
            })
        }
        labels = {
            "account": "Hesap",
            "category": "Transfer Kategorisi",
            "amount": "Miktar",
            "description": "Not",
        }

    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["account"].queryset = Account.objects.filter(
                user=user, is_active=True
            )

            self.fields["category"].queryset = Category.objects.filter(
                user=user,
                is_active=True,
                is_parent=False,
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.currency = instance.account.currency

        if commit:
            instance.save()

        return instance
    
    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Amount must be positive.")
        return amount
