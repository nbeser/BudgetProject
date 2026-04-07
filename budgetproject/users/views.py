from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, UserSignupForm




def user_login(request):
    if request.user.is_authenticated:
        return redirect("pages_index")
    
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()     
            login(request, user)
            
            return redirect("user_dashboard")
        
        else:
            form.add_error(None, "Geçersiz email yada şifre.")
    else:
        form = UserLoginForm()
    
    return render(request, "users/login.html", {"form": form})


def user_register(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_login")
    else:
        form = UserSignupForm()
    return render(request, "users/signup.html", {"form": form})
        


def user_logout(request):
    logout(request)
    return redirect("user_login")