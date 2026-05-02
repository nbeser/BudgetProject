from datetime import date
from django.db import transaction

from transaction.models import Transaction
from .models import RecurringTransaction

from django.utils import timezone

import calendar

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
        last_day = calendar.monthrange(today.year, today.month)[1]
        run_day = min(rule.start_date.day, last_day)
        return today.day == run_day

    if rule.frequency == "yearly":
        return (
            today.day == rule.start_date.day
            and today.month == rule.start_date.month
        )

    return False

def run_recurring_transactions():

    today = timezone.localdate()

    recurring_rules = RecurringTransaction.objects.filter(
        is_active=True,
        start_date__lte=today
    ).select_related("user", "account", "category")

    with transaction.atomic():
        for i in recurring_rules:

            if not should_run(i, today):
                continue
            if Transaction.objects.filter(
                recurring_rule=i,
                transaction_date__date=today
            ).exists():
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
                transaction_date=timezone.now(),
                recurring_rule=i
            )

            i.last_run = today
            i.save()