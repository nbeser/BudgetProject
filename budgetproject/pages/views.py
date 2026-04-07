from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone

from transaction.models import Transaction
from account.models import Account


def pages_index(request):
    return render(request, "pages/index.html")


@login_required()
def user_dashboard(request):
    user = request.user
    today = timezone.now()

    transactions = Transaction.objects.filter(user=user)

    monthly_transactions = transactions.filter(transaction_date__year=today.year, transaction_date__month=today.month)

    income = monthly_transactions.filter(
        category__type="income"
    ).aggregate(total=Sum("amount"))["total"] or 0

    expense = monthly_transactions.filter(
        category__type="expense"
    ).aggregate(total=Sum("amount"))["total"] or 0

    accounts = Account.objects.filter(user=user, is_active=True)
    total_balance = sum(account.balance for account in accounts)

    recent_transactions = transactions.order_by("-transaction_date")[:5]

    context = {
        "aylik_islem": monthly_transactions,
        "gelir": income,
        "gider": expense,
        "toplam": total_balance,
        "son_islemler": recent_transactions
    }
    
    return render(request, "pages/dashboard.html", context)