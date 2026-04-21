from django.conf import settings
from django.db import models

from account.models import Account
from category.models import Category

from django.core.exceptions import ValidationError

from transaction.models import Transaction
from django.db.models import Sum
from django.utils import timezone


class Budget(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budgets")

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="budgets")

    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name="budgets")

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

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
        categories = [self.category]

        children = self.category.children.all()
        if children.exists():
            categories += list(children)

        transactions = Transaction.objects.filter(
            user=self.user,
            category__in=categories,
            transaction_date__gte=self.start_date,
            transaction_date__lte=self.end_date,
        )

        if self.account:
            transactions = transactions.filter(account=self.account)

       
        '''
        print("------ DEBUG ------")
        print("Budget start:", self.start_date)
        print("Budget end:", self.end_date)

        all_user_tx = Transaction.objects.filter(user=self.user)
        print("ALL user transactions:", all_user_tx.count())
        print("ALL dates:", list(all_user_tx.values_list("transaction_date", flat=True)))

        filtered = Transaction.objects.filter(
            user=self.user,
            category__in=categories,
        )
        print("After category filter:", filtered.count())

        date_filtered = filtered.filter(
            transaction_date__gte=self.start_date,
            transaction_date__lte=self.end_date,
        )
        print("After date filter:", date_filtered.count())

        if self.account:
            acc_filtered = date_filtered.filter(account=self.account)
            print("After account filter:", acc_filtered.count())

        print("Budget category:", self.category.id)
        print("Categories used:", [c.id for c in categories])
        print("Transaction categories:", list(all_user_tx.values_list("category_id", flat=True)))

        print("-------------------")
        '''

        '''
        print("------ FINAL CHECK ------")
        print("Budget start (UTC):", self.start_date)
        print("Budget start (LOCAL):", timezone.localtime(self.start_date))

        for t in Transaction.objects.filter(user=self.user)[:5]:
            print("TX UTC:", t.transaction_date, "| LOCAL:", timezone.localtime(t.transaction_date))

        print("-------------------------")
        '''




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