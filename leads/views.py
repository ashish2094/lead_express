from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from .models import Leads
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
import datetime
import xlwt

# Create your views here.
class LeadView(View):
    def get(self, request):
        data = []
        data = Leads.objects.all().order_by('-date')
        p = Paginator(data, 10)
        page_no = request.GET.get('page')
        page_obj = Paginator.get_page(p, page_no)
        context = {
            'data': data,
            'page_obj' : page_obj,
        }
        return render(request, 'leads.html', context)

class LeadAddView(View):
    def get(self, request):
        context = {
        }
        print(context)
        return render(request, "leadadd.html", context)

    def post(self, request):
        outlet = request.POST['outlet']
        zone = request.POST['zone']
        coordinates = request.POST['coordinates']
        timing = request.POST['timing']
        address = request.POST['address']
        remark = request.POST['remark']
        Leads.objects.create(author=request.user, outlet = outlet, 
            zone = zone,timings = timing, coordinates = coordinates, address = address, remark = remark)
        messages.info(request, 'New Lead Created!')
        return redirect('/leads')

class Exportxl(View):
    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename= Leads' + str(datetime.datetime.now()) + '.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Leads')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold=True
        cols = ['Outlet', 'Zone', 'Coordinates', 'Timings', 'Address', 'Remark', 'Date']
        for col_n in range(len(cols)):
            ws.write(row_num, col_n, cols[col_n], font_style)
        font_style = xlwt.XFStyle()
        rows = Leads.objects.all().order_by('-date').values_list('outlet', 'zone', 'coordinates', 'timings', 'address', 'remark', 'date')
        for row in rows:
            row_num += 1
            for col_n in range(len(row)):
                ws.write(row_num, col_n, str(row[col_n]), font_style)
        wb.save(response)
        return response
