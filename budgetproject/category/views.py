from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category
from .forms import CreateCategoryForm




@login_required
def category_register(request):
    if request.method == "POST":
        form = CreateCategoryForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("operations")
    else:
        form = CreateCategoryForm(user=request.user)
    return render(request, "category/create_category.html", {"form": form})



@login_required
def category_edit(request):
    pass


@login_required
def category_delete(request):
    pass