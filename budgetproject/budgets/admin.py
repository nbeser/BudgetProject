from django.contrib import admin

from category.models import Category

from .models import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "category",
        "account",
        "amount",
        "start_date",
        "end_date",
        "is_active",
    )

    list_filter = ("user", "category", "is_active")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(
                user=request.user,
                type="expense",
                is_active=True
            )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)