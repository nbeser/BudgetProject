from django import forms
from django.contrib.auth import get_user_model
from .models import RecurringTransaction

from account.models import Account
from category.models import Category


User = get_user_model()


class RecurringForm(forms.ModelForm):

    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', "class": "form-control"})
    )
    last_run = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', "class": "form-control"})
    )

    class Meta:
        model = RecurringTransaction
        fields = ("account", "category", "amount", "currency", "description", "frequency", "start_date", "last_run", "is_active")
        widgets = {
            "account": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0,00"}),
            "currency": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Hatırlatıcı not..."
            }),
            "frequency": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput()
        }



        labels = {
            "account": "Hesap",
            "category": "Transfer Kategorisi",
            "amount": "Miktar",
            "currency": "Yatırım Tipi",
            "description": "Not...",
            "frequency": "İşlem Sıklığı",
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