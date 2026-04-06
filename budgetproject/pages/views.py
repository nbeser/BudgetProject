from django.shortcuts import render


def pages_index(request):
    return render(request, "pages/index.html")