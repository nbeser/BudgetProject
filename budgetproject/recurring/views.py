from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RecurringForm

from .models import RecurringTransaction


@login_required
def recurring_register(request):
    if request.method == "POST":
        form = RecurringForm(request.POST, user=request.user)
        if form.is_valid():
            recurring = form.save(commit=False)   
            recurring.user = request.user
            recurring.save()
            return redirect("operations")
    else:
        form = RecurringForm(user=request.user)

    return render(request, "recurring/create_recurring.html", {"form": form})


@login_required
def recurring_edit(request, pk):
    recurring = get_object_or_404(RecurringTransaction, pk=pk, user=request.user)
    if request.method == "POST":
        form = RecurringForm(request.POST, request.FILES, user=request.user, instance=recurring)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect("operations")
    else:
        form = RecurringForm(user=request.user, instance=recurring)
    return render(request, "recurring/edit_recurring.html", {"form": form})




@login_required
def recurring_delete(request, pk):
    recurring = get_object_or_404(RecurringTransaction, pk=pk, user=request.user)
    if request.method == "POST":
        recurring.delete()
        return redirect("operations")
    return render(request, "recurring/delete_recurring.html", {"recurring": recurring})