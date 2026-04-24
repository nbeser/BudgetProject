from django import forms
from django.contrib.auth import get_user_model
from .models import Budget

from account.models import Account
from category.models import Category
from django.utils import timezone

User = get_user_model()


class CreateBudgets(forms.ModelForm):
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', "class": "form-control"})
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', "class": "form-control"})
    )
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class":"form-control"
        })
    )
    class Meta:
        model = Budget
        fields = ("category", "account", "amount", "start_date", "end_date", "is_active")
        widgets = {
            "category": forms.Select(attrs={"class": "form-control"}),
            "account": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["category"].queryset = Category.objects.filter(user=self.user, type=Category.CategoryType.EXPENSE)
            self.fields["account"].queryset = Account.objects.filter(user=self.user)

    def clean(self):
        cleaned_data = super().clean()

        if self.user:
            self.instance.user = self.user

        return cleaned_data
    
    # def clean_start_date(self):
    #     dt = self.cleaned_data["start_date"]
    #     if timezone.is_naive(dt):
    #         return timezone.make_aware(dt, timezone.get_current_timezone())
    #     return dt

    # def clean_end_date(self):
    #     dt = self.cleaned_data["end_date"]
    #     if timezone.is_naive(dt):
    #         return timezone.make_aware(dt, timezone.get_current_timezone())
    #     return dt


class EditBudgets(forms.ModelForm):
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', "class": "form-control"})
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', "class": "form-control"})
    )
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class":"form-control"
        })
    )
    class Meta:
        model = Budget
        fields = ("category", "account", "amount", "start_date", "end_date", "is_active")
        widgets = {
            "category": forms.Select(attrs={"class": "form-control"}),
            "account": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(),
        }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["category"].queryset = Category.objects.filter(user=self.user, type=Category.CategoryType.EXPENSE)
            self.fields["account"].queryset = Account.objects.filter(user=self.user)
    
    # def clean_start_date(self):
    #     dt = self.cleaned_data["start_date"]
    #     if timezone.is_naive(dt):
    #         return timezone.make_aware(dt, timezone.get_current_timezone())
    #     return dt

    # def clean_end_date(self):
    #     dt = self.cleaned_data["end_date"]
    #     if timezone.is_naive(dt):
    #         return timezone.make_aware(dt, timezone.get_current_timezone())
    #     return dt
