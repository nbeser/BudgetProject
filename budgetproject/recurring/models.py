from django.db import models
from django.conf import settings
import uuid

from django.utils import timezone


from account.models import Account
from category.models import Category

from django.core.exceptions import ValidationError


class RecurringTransaction(models.Model):

    class Frequency(models.TextChoices):
        DAILY = "daily", "Daily"
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"
        YEARLY = "yearly", "Yearly"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recurring_transactions")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="recurring_transactions")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recurring_transactions")
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=3, db_index=True)
    description = models.TextField(blank=True)

    frequency = models.CharField(max_length=20, choices=Frequency.choices)

    start_date = models.DateField(default=timezone.now)
    last_run = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.account.user_id != self.user_id:
            raise ValidationError("Account must belong to the same user.")

        if self.category.user_id != self.user_id:
            raise ValidationError("Category must belong to the same user.")
        
        if self.category.is_parent:
            raise ValidationError("Cannot assign transaction to parent category.")
  
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.currency} ({self.frequency})"