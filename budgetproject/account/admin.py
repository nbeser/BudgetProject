from django.contrib import admin
from .models import Account
from django import forms

class AccountAdminForm(forms.ModelForm):
    opening_balance = forms.DecimalField(
        max_digits=14,
        decimal_places=2,
        required=False
    )

    class Meta:
        model = Account
        fields = "__all__"

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "account_type", "currency", "balance", "is_active",)
    list_filter = ("currency", "account_type",)
    search_fields = ("name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    form = AccountAdminForm

    def save_model(self, request, obj, form, change):
        if not change:
            obj._opening_balance = form.cleaned_data.get("opening_balance")
        super().save_model(request, obj, form, change)
        
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is not None:  # editing existing account
            form.base_fields.pop("opening_balance", None)
        return form