from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CreateTransactionForm



@login_required
def transaction_register(request):
    if request.method == "POST":
        form = CreateTransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)   
            transaction.user = request.user
            transaction.save()
            return redirect("operations")
    else:
        form = CreateTransactionForm(user=request.user)

    return render(request, "transaction/create_transaction.html", {"form": form})