from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Account

from .forms import CreateAccount, UpdateAccount


@login_required
def account_register(request):
    if request.method == "POST":
        form = CreateAccount(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect("user_dashboard")
    else:
        form = CreateAccount()
    return render(request, "account/create_account.html", {"form": form})


@login_required
def account_edit(request, id):
    account = get_object_or_404(Account, id=id)
    if request.method == "POST":
        form = UpdateAccount(request.POST, request.FILES, instance=account)
        form.save()
        return redirect("user_dashboard")
    else:
        form = UpdateAccount(instance=account)
    return render(request, "account/edit_account.html", {"form": form})


@login_required
def account_delete(request, id):
    account = get_object_or_404(Account, id=id)
    if request.method == "POST":
        account.delete()
        return redirect("user_dashboard")
    return render(request, "account/delete_account.html", {"account": account})
    