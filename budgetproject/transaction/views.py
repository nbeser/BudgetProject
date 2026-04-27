from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from .models import Transaction



@login_required
def transaction_register(request):
    if request.method == "POST":
        form = TransactionForm(request.POST, user=request.user, mode="create")
        if form.is_valid():
            transaction = form.save(commit=False)   
            transaction.user = request.user
            transaction.save()
            return redirect("operations")
    else:
        form = TransactionForm(user=request.user)

    return render(request, "transaction/create_transaction.html", {"form": form})



@login_required
def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        form = TransactionForm(request.POST, request.FILES, user=request.user, instance=transaction, mode="edit")
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect("operations")
    else:
        form = TransactionForm(user=request.user, instance=transaction)
    return render(request, "transaction/edit_transaction.html", {"form": form})



@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user, mode="delete")
    if request.method == "POST":
        transaction.delete()
        return redirect("operations")
    return render(request, "transaction/delete_transaction.html", {"transaction": transaction})
    