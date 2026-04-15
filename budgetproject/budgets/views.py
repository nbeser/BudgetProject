from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Budget
from .forms import CreateBudgets, EditBudgets


@login_required
def budget_register(request):
    if request.method == "POST":
        form = CreateBudgets(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("get_budget")
    else:
        form = CreateBudgets(user=request.user)
    return render(request, "budgets/create_budgets.html", {"form": form})



@login_required
def budget_edit(request, id):
    budget = get_object_or_404(Budget, id=id)
    if request.method == "POST":
        form = EditBudgets(request.POST, request.FILES, instance=budget)
        form.save()
        return redirect("get_budget")
    else:
        form = EditBudgets(user=request.user)
    return render(request, "budgets/edit_budgets.html", {"form": form})