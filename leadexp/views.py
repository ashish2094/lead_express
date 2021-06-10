from leads.models import Leads, Status, Zone

from django.shortcuts import render, redirect


def home_view(request):
    context = {}
    return render(request, 'home.html', context)


def contact_view(request):
    context = {}
    return render(request, 'Contact.html', context)


def dashboard_view(request):
    data = Leads.objects.filter(author=request.user,status=2).order_by('-date')[:5][::-1]
    new_l = Leads.objects.filter(author=request.user, status=1).count()
    k_audit = Leads.objects.filter(author=request.user, status=5).count()
    signed = Leads.objects.filter(author=request.user, status=6).count()
    brands = Leads.objects.filter(author=request.user, status=7).count()
    context = {
        "data": data,
        "new_l": new_l,
        "k_audit": k_audit,
        "signed": signed,
        "brands": brands,
    }
    return render(request, 'auth/dash.html', context)