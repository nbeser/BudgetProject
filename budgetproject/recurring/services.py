from datetime import date
from django.db import transaction

from transaction.models import Transaction
from .models import RecurringTransaction

def should_run(rule, today):

    if rule.last_run == today:
        return False

    if today < rule.start_date:
        return False

    if rule.frequency == "daily":
        return True

    if rule.frequency == "weekly":
        return today.weekday() == rule.start_date.weekday()

    if rule.frequency == "monthly":
        return today.day == rule.start_date.day

    if rule.frequency == "yearly":
        return (
            today.day == rule.start_date.day
            and today.month == rule.start_date.month
        )

    return False

def run_recurring_transactions():

    today = date.today()

    recurring_rules = RecurringTransaction.objects.filter(is_active=True)

    for i in recurring_rules:

        if not should_run(i, today):
            continue
        # if i.last_run == today:
        #     continue

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