from django.core.management.base import BaseCommand, CommandError
from recurring.models import RecurringTransaction
from recurring.services import run_recurring_transactions

class Command(BaseCommand):
    help = "Runs recurring transaction engine"

    def handle(self, *args, **options):
        self.stdout.write("Running recurring transaction engine")
        run_recurring_transactions()
        self.stdout.write(
            self.style.SUCCESS("Recurring transactions processed successfully.")
        )