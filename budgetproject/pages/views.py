from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from django.db.models import Sum, Case, When, F, DecimalField

from transaction.models import Transaction
from account.models import Account
from budgets.models import Budget
from category.models import Category
from recurring.models import RecurringTransaction


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
    total_by_account = [(i.name.capitalize(), i.balance, i.currency.upper(), i.name, i.id) for i in accounts ]
    total_balance = sum(account.balance for account in accounts)

    recent_transactions = transactions.order_by("-transaction_date")[:5]

    context = {
        "hesaplar": accounts,
        "aylik_islem": monthly_transactions,
        "gelir": income,
        "gider": expense,
        "toplam": total_balance,
        "toplam_hesap": total_by_account,
        "son_islemler": recent_transactions,  
        "secili_hesap": [(i.name for i in accounts)],
    }
    
    return render(request, "pages/dashboard.html", context)


@login_required()
def get_budget(request):
    user = request.user
    budgets = Budget.objects.filter(user=user, is_active=True)
    accounts = Account.objects.filter(user=user, is_active=True)
    total_by_account = [(i.name.capitalize(), i.balance, i.currency.upper(), i.name, i.id) for i in accounts ]


    context = {
        "hesaplar": accounts,
        "budgets": budgets,
        "toplam_hesap": total_by_account,
        "secili_hesap": [(i.name for i in accounts)],
    }
    return render(request, "pages/budgets.html", context)



@login_required
def accounts(request, id):
    user = request.user
    accounts = Account.objects.filter(user=user, is_active=True)
    account = Account.objects.get(user=user, is_active=True, id=id)
    transactions = Transaction.objects.filter(user=user, account__id=id)
    account_transactions = transactions.order_by("-transaction_date")

    summary = account.transaction_account.aggregate(
        income=Sum(
            Case(
                When(category__type="income", then=F("amount")),
                output_field=DecimalField()
            )
        ),
        expense=Sum(
            Case(
                When(category__type="expense", then=F("amount")),
                output_field=DecimalField()
            )
        )
    )

    income = summary["income"] or 0
    expense = summary["expense"] or 0

    total_by_account = [(i.name.capitalize(), i.balance, i.currency.upper(), i.name, i.id) for i in accounts]

    context = {
        "hesap": account,
        "acilis": account.created,
        "toplam_hesap": total_by_account,
        "income": float(income),
        "expense": float(expense),
        "son_islemler": account_transactions,
        "secili_hesap": account.name,
    }

    return render(request, "pages/accounts.html", context)



@login_required
def operations(request):
    return render(request, "pages/operations.html")


@login_required
def operations_popup(request, key):
    budgets = Budget.objects.filter(user=request.user)
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user, category__is_system=False).order_by("-created")
    categories = Category.objects.filter(user=request.user, is_system=False)
    recurrings = RecurringTransaction.objects.filter(user=request.user)

    data = {
        "budgets": budgets,
        "accounts": accounts,
        "transactions": transactions,
        "categories": categories,
        "recurrings": recurrings,
    }

    return render(request, "pages/operations_popup.html", {
        "items": data.get(key, []),
        "key": key,
    })
