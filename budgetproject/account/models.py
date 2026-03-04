from django.db import models
from django.conf import settings
from django.db.models import Sum, Case, When, F, DecimalField
from category.models import Category
from django.db import transaction as db_transaction


ACCOUNT_TYPES = [
    ("cash", "Cash"),
    ("bank", "Bank"),
    ("credit", "Credit Card"),
    ("investment", "Investment"),
]


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts")
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default="cash")
    currency = models.CharField(max_length=3, db_index=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "name"], name="unique_user_account_name")
        ]

        indexes = [
            models.Index(fields=["user", "is_active"]),
        ]

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        opening_balance = getattr(self, "_opening_balance", None)
        if self.currency:
            self.currency = self.currency.upper()

        with db_transaction.atomic():
            super().save(*args, **kwargs)

            if is_new and opening_balance and opening_balance != 0:
                category, _ = Category.objects.get_or_create(
                    user=self.user,
                    name="Opening Balance",
                    type=Category.CategoryType.INCOME,
                    parent=None,
                    defaults={"is_system": True},
                )

                from transaction.models import Transaction

                Transaction.objects.create(
                    user=self.user,
                    account=self,
                    category=category,
                    amount=opening_balance,
                    currency=self.currency,
                    transaction_date=self.created,
                    description="Opening Balance"
                )
   
    @property
    def balance(self):
        total = self.transaction_account.aggregate(
            total=Sum(
                Case(
                    When(category__type="income", then=F("amount")),
                    When(category__type="expense", then=-F("amount")),
                    output_field=DecimalField()
                )
            )
        )["total"]
        return total or 0

    def __str__(self):
        return f"{self.name} ({self.user.username})"