from django.shortcuts import render, redirect

def home_view(request):
    context ={}
    return render(request, 'home.html', context)

def contact_view(request):
    context ={}
    return render(request, 'Contact.html', context)

def dashboard_view(request):
    context ={}
    return render(request, 'auth/dash.html', context)