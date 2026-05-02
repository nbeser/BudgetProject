from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Category(models.Model):

    class CategoryType(models.TextChoices):
        INCOME = "income", "Income"
        EXPENSE = "expense", "Expense"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CategoryType.choices)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children")
    is_system = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "name", "type"], name="unique_user_category_name")
        ]
        indexes = [
            models.Index(fields=["user", "type"])
        ]
    
    def clean(self):
        if self.parent:
            if self.parent.user != self.user:
                raise ValidationError("Parent category must belong to same user.")

            if self.parent.parent:
                raise ValidationError("Only one level of nesting allowed.")
            
    def save(self, *args, **kwargs):

        if self.parent:
            if self.parent.recurring_transactions.exists():
                raise ValidationError(
                    "Cannot assign this parent because it is used in recurring transactions."
                )

        if self.parent:
            Category.objects.filter(id=self.parent.id).update(is_parent=True)
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name} ({self.user.name})"
        return f"{self.name} ({self.user.name})"