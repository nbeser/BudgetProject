from django.db import models
from django.conf import settings

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
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)

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
        if self.currency:
            self.currency = self.currency.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.currency})"