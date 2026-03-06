from django.contrib import admin

from .models import RecurringTransaction


@admin.register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "account",
        "category",
        "amount",
        "currency",
        "frequency",
        "start_date",
        "last_run",
        "is_active",
    )

    list_filter = (
        "frequency",
        "is_active",
        "currency",
    )

    search_fields = (
        "description",
        "user__username",
        "account__name",
    )