from django.conf import settings
from django.db import models

from account.models import Account
from category.models import Category

from django.core.exceptions import ValidationError

from transaction.models import Transaction
from django.db.models import Sum


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
        

    @property
    def spent_amount(self):

        transactions = Transaction.objects.filter(
            user=self.user,
            category=self.category,
            transaction_date__gte=self.start_date,
            transaction_date__lte=self.end_date,
        )

        if self.account:
            transactions = transactions.filter(account=self.account)

        total = transactions.aggregate(total=Sum("amount"))["total"]

        return total or 0

    @property
    def remaining_amount(self):
        return self.amount - self.spent_amount
    
    @property
    def progress_percentage(self):

        if self.amount == 0:
            return 0

        return (self.spent_amount / self.amount) * 100


    def __str__(self):
        return f"{self.category.name} - {self.amount}"