from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from .forms import CreateAccount


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