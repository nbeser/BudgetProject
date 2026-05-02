from django.db import models
import uuid
from django.conf import settings
from account.models import Account
from category.models import Category
from django.core.exceptions import ValidationError
from django.utils import timezone

from recurring.models import RecurringTransaction
from django.db.models.functions import TruncDate

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transaction_account")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="transaction_category")
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)  
    currency = models.CharField(max_length=3, db_index=True)

    description = models.TextField(blank=True, null=True)
    transaction_date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    recurring_rule = models.ForeignKey(RecurringTransaction, null=True, blank=True, on_delete=models.SET_NULL)

    def clean(self):

        if not self.user_id or not self.account_id or not self.category_id:
            return

        if self.account.user_id != self.user_id:
            raise ValidationError("Account must belong to the same user.")

        if self.category.user_id != self.user_id:
            raise ValidationError("Category must belong to the same user.")

        if self.category.is_parent:
            raise ValidationError("Cannot assign transaction to parent category.")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                TruncDate("transaction_date"),
                "recurring_rule",
                name="unique_recurring_per_day"
            )
        ]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.account.name} - {self.amount} {self.currency}"