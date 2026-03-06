from datetime import date
from django.db import transaction

from transaction.models import Transaction
from .models import RecurringTransaction


def run_recurring_transactions():

    today = date.today()

    recurring_rules = RecurringTransaction.objects.filter(
        is_active=True
    )

    for i in recurring_rules:

        if i.last_run == today:
            continue

        Transaction.objects.create(
            user=i.user,
            account=i.account,
            category=i.category,
            amount=i.amount,
            currency=i.currency,
            description=i.description,
            transaction_date=today
        )

        i.last_run = today
        i.save()