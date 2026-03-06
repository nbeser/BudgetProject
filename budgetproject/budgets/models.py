from django.conf import settings
from django.db import models

from account.models import Account
from category.models import Category

from django.core.exceptions import ValidationError


class Budget(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budgets")

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="budgets")

    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name="budgets")

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    start_date = models.DateField()
    end_date = models.DateField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.category.type != "expense":
            raise ValidationError("Budgets can only be set for expense categories.")
        
        if self.account and self.account.user != self.user:
            raise ValidationError("Account must belong to the same user.")

        if self.category.user != self.user:
            raise ValidationError("Category must belong to the same user.")

    def __str__(self):
        return f"{self.category.name} - {self.amount}"