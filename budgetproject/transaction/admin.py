from django.contrib import admin
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    