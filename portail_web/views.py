from django.shortcuts import render

def home(request):
    return render(request, 'libs/home.html') 

def about(request):
    return render(request, 'libs/about.html')