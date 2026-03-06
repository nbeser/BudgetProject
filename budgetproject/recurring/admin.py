from django.contrib import admin

from category.models import Category

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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(
                user=request.user,
                is_system=False
            )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)