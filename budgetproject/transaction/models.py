from django.db import models
import uuid
from django.conf import settings
from account.models import Account
from category.models import Category
from django.core.exceptions import ValidationError
from django.utils import timezone


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

    def clean(self):
        if self.account.user != self.user:
            raise ValidationError("Account must belong to the same user.")

        if self.category.user != self.user:
            raise ValidationError("Category must belong to the same user.")

        if self.category.is_parent:
            raise ValidationError("Cannot assign transaction to parent category.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.account.name} - {self.amount} {self.currency}"