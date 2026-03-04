from django.contrib import admin

from category.models import Category
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "account",
        "category",
        "amount",
        "currency",
        "transaction_date",
        "user",
    )
    list_filter = ("currency", "transaction_date")
    search_fields = ("description",)
    date_hierarchy = "transaction_date"

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(user=request.user)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            if request.user.is_superuser:
                kwargs["queryset"] = Category.objects.filter(is_system=False)
            else:
                kwargs["queryset"] = Category.objects.filter(
                    user=request.user,
                    is_system=False
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)