from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from .models import Leads
from .resources import LeadResource
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
import datetime
from tablib import Dataset
import xlwt

# Create your views here.
class LeadView(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    def get(self, request):
        data = []
        data = Leads.objects.filter(author=request.user).order_by('-date')
        p = Paginator(data, 10)
        page_no = request.GET.get('page')
        page_obj = Paginator.get_page(p, page_no)
        context = {
            'data': data,
            'page_obj' : page_obj,
        }
        return render(request, 'leads.html', context)

class LeadAddView(LoginRequiredMixin, View):
    login_url = '/auth/login/'
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
        response['Content-Disposition'] = 'attachment; filename= Leads' + str(datetime.date.today()) + '.xls'
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

class Importxl(View):
    def get(self, request):
        return render(request, "upload.html", {})

    def post(self, request):
        lead_resource = LeadResource()
        dataset = Dataset()
        new_lead = request.FILES['myfile']
        if not new_lead.name.endswith('xlsx' or 'xls'):
            messages.info(request, 'Unsupported Format')
            return redirect('/import-excel/')
        if new_lead.name.endswith('xlsx'):
            imported_data = dataset.load(new_lead.read(), format='xlsx')
        if new_lead.name.endswith('xls'):
            imported_data = dataset.load(new_lead.read(), format='xls')
        for data in imported_data:
            print(data)

            Leads.objects.create(author=request.user, outlet = data[1], 
            zone = data[2],coordinates = data[3], timings = data[4],address = data[5])
        context={}
        return redirect('/leads')

class EditLeadView(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    def get(self, request, id):
        lead = Leads.objects.get(author=request.user, pk=id)
        context = {
            'lead' : lead,
            }
        return render(request, "editlead.html", context)

    def post(self, request, id):
        outlet = request.POST['outlet']
        if not outlet:
            messages.error(request, 'Outlet Required')
            return redirect('/leads/')
        zone = request.POST['zone']
        coordinates = request.POST['coordinates']
        time = request.POST['timings']
        address = request.POST['address']
        remark = request.POST['remark']
        lead = Leads.objects.get(id=id)
        lead.author=request.user
        lead.outlet = outlet
        lead.zone = zone
        lead.address = address
        lead.remark = remark
        lead.coordinates = coordinates
        lead.timings = time
        lead.save()
        messages.info(request, 'Lead Updated Successfully!')
        return redirect('/leads/')

class DeleteLeadView(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    def get(self, request, id):
        lead = Leads.objects.get(id=id)
        lead.delete()
        messages.info(request, 'Lead Deleted Successfully!')
        return redirect('/leads/')
