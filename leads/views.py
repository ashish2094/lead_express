from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from .models import Leads, Status, Zone
from .resources import LeadResource
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
import datetime
from tablib import Dataset
import xlwt
import xlrd


# Create your views here.
class LeadView(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def get(self, request):
        data = []
        data = Leads.objects.filter(author=request.user,
                                    status='1').order_by('-date')
        option = Status.objects.all()
        zone = Zone.objects.all()
        p = Paginator(data, 10)
        page_no = request.GET.get('page')
        page_obj = Paginator.get_page(p, page_no)
        context = {
            'data': data,
            'option': option,
            'zone': zone,
            'page_obj': page_obj,
        }
        return render(request, 'lead/leads.html', context)

    def post(self, request):
        s = request.POST['zone']
        if s == 'All':
            return redirect('/leads/')
        z = Zone.objects.get(zone=s)
        data = []
        data = Leads.objects.filter(author=request.user,
                                    zone=z.id).order_by('-date')
        option = Status.objects.all()
        zone = Zone.objects.all()
        p = Paginator(data, 10)
        page_no = request.GET.get('page')
        page_obj = Paginator.get_page(p, page_no)
        context = {
            'data': data,
            'zone': zone,
            'page_obj': page_obj,
        }
        return render(request, 'lead/leads.html', context)


class LeadAddView(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def get(self, request):
        option = Status.objects.all()
        zone = Zone.objects.all()
        context = {
            'option': option,
            'zone': zone,
        }
        return render(request, "lead/leadadd.html", context)

    def post(self, request):
        outlet = request.POST['outlet']
        z = request.POST['zone']
        zone = Zone.objects.get(zone=z)
        coordinates = request.POST['coordinates']
        timing = request.POST['timing']
        address = request.POST['address']
        owner = request.POST['owner']
        contact = request.POST['contact']
        option = request.POST['option']
        if option == 'New':
            Leads.objects.create(author=request.user,
                                 outlet=outlet,
                                 owner=owner,
                                 contact=contact,
                                 zone=zone,
                                 timings=timing,
                                 coordinates=coordinates,
                                 address=address)
        else:
            status = Status.objects.get(option=option)
            Leads.objects.create(author=request.user,
                                 outlet=outlet,
                                 owner=owner,
                                 contact=contact,
                                 zone=zone,
                                 timings=timing,
                                 coordinates=coordinates,
                                 address=address,
                                 status=status)
        messages.info(request, 'New Lead Created!')
        return redirect('/leads')


class LeadInterested(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def get(self, request):
        data = []
        data = Leads.objects.filter(author=request.user).exclude(
            status=1).exclude(status=3).order_by('-date')
        option = Status.objects.all()
        p = Paginator(data, 10)
        page_no = request.GET.get('page')
        page_obj = Paginator.get_page(p, page_no)
        context = {
            'data': data,
            'option': option,
            'page_obj': page_obj,
        }
        return render(request, 'lead/leads_interested.html', context)

    def post(self, request):
        o = request.POST['option']
        if o == 'All':
            return redirect('/leads/ok/')
        opt = Status.objects.get(option=o)
        option = Status.objects.all()
        data = Leads.objects.filter(author=request.user,
                                    status=opt.id).order_by('-date')
        p = Paginator(data, 10)
        page_no = request.GET.get('page')
        page_obj = Paginator.get_page(p, page_no)
        context = {
            'data': data,
            'option': option,
            'page_obj': page_obj,
        }
        return render(request, 'lead/leads_interested.html', context)


class LeadUninterested(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def get(self, request):
        data = []
        data = Leads.objects.filter(author=request.user,
                                    status=3).order_by('-date')
        option = Status.objects.all()
        p = Paginator(data, 10)
        page_no = request.GET.get('page')
        page_obj = Paginator.get_page(p, page_no)
        context = {
            'data': data,
            'option': option,
            'page_obj': page_obj,
        }
        return render(request, 'lead/leads_not.html', context)


class Exportxl(View):
    def get(self, request):
        columns = request.GET.getlist('checks')
        date_min = request.GET['min-date']
        date_max = request.GET['max-date']
        qs = Leads.objects.filter(
            author=request.user).order_by('-date').values_list(*columns)
        try:
            qs = qs.filter(date__gte=date_min)
            qs = qs.filter(date__lte=date_max)
        except:
            messages.error(request, 'Date Required')
            return redirect('/import-excel/')
        z_index = 'a'
        s_index = 'a'
        if 'zone' in columns:
            z = request.GET['zone']
            z_index = columns.index('zone')
            if z != 'All':
                zone = Zone.objects.get(zone=z)
                qs = qs.filter(zone=zone.id)
        if 'status' in columns:
            s = request.GET['option']
            s_index = columns.index('status')
            if s != 'All':
                status = Status.objects.get(option=s)
                qs = qs.filter(status=status.id)
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename= Leads-' + str(
            datetime.date.today()) + '.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Leads')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        cols = []
        cols.append('Sr.No.')
        for c in columns:
            cols.append(c.capitalize())
        for col_n in range(len(cols)):
            ws.write(row_num, col_n, cols[col_n], font_style)
        font_style = xlwt.XFStyle()
        rows = qs
        print("z=", z_index, ", s=", s_index)
        for row in rows:
            row_num += 1
            ws.write(row_num, 0, str(row_num), font_style)
            for col_n in range(len(row)):
                if col_n == z_index:
                    try:
                        ws.write(row_num, col_n + 1,
                                 str(Zone.objects.get(id=row[col_n]).zone),
                                 font_style)
                    except:
                        ws.write(row_num, col_n + 1, '', font_style)
                elif col_n == s_index:
                    try:
                        ws.write(row_num, col_n + 1,
                                 str(Status.objects.get(id=row[col_n]).option),
                                 font_style)
                    except:
                        ws.write(row_num, col_n + 1, '', font_style)
                else:
                    ws.write(row_num, col_n + 1, str(row[col_n]), font_style)
        wb.save(response)
        return response


class Importxl(View):
    def get(self, request):
        option = Status.objects.all()
        zone = Zone.objects.all()
        context = {
            'option': option,
            'zone': zone,
        }
        return render(request, "lead/upload.html", context)

    def post(self, request):
        lead_resource = LeadResource()
        dataset = Dataset()
        new_lead = request.FILES['myfile']
        if not new_lead.name.endswith('xlsx'):
            if not new_lead.name.endswith('xls'):
                messages.info(request, 'Unsupported Format')
                return redirect('/import-excel/')
        if new_lead.name.endswith('xlsx'):
            imported_data = dataset.load(new_lead.read(), format='xlsx')
        if new_lead.name.endswith('xls'):
            imported_data = dataset.load(new_lead.read(), format='xls')
        head = imported_data.headers
        if None in head:
            messages.info(
                request,
                'Error in heading, try removing vacant rows and coloumns.')
            return redirect('/import-excel/')
        for data in imported_data:
            if not data[1]:
                continue
            else:
                if 'Outlet' in head:
                    outlet_index = head.index('Outlet')
                else:
                    messages.error(request, 'Outlet Column Required')
                    return redirect('/import-excel/')
                if 'Zone' in head:
                    zi = head.index('Zone')
                    try:
                        zone = Zone.objects.get(zone=data[zi])
                    except:
                        Zone.objects.create(zone=data[zi])
                        zone = Zone.objects.get(zone=data[zi])
                else:
                    messages.error(request, 'Zone Column Required')
                    return redirect('/import-excel/')
                if 'Owner' in head:
                    oi = head.index('Owner')
                    owner = data[oi]
                else:
                    owner = ''
                if 'Contact' in head:
                    ci = head.index('Contact')
                    contact = data[ci]
                else:
                    contact = ''
                if 'Coordinates' in head:
                    cooi = head.index('Coordinates')
                    coordinates = data[cooi]
                else:
                    coordinates = ''
                if 'Timings' in head:
                    ti = head.index('Timings')
                    timings = data[ti]
                else:
                    timings = ''
                if 'Address' in head:
                    ai = head.index('Address')
                    address = data[ai]
                else:
                    address = ''
                if 'Status' in head:
                    si = head.index('Status')
                    status = Status.objects.get(option=data[si])
                else:
                    status = Status.objects.get(id=1)
                try:
                    Leads.objects.create(author=request.user,
                                         outlet=data[outlet_index],
                                         zone=zone,
                                         owner=owner,
                                         contact=contact,
                                         coordinates=coordinates,
                                         timings=timings,
                                         address=address,
                                         status=status)
                except:
                    messages.error(request, 'Error Occoured')
                    return redirect('/import-excel/')
        context = {}
        return redirect('/leads')


class EditLeadView(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def get(self, request, id):
        lead = Leads.objects.get(author=request.user, pk=id)
        option = Status.objects.all()
        zone = Zone.objects.all()
        context = {
            'lead': lead,
            'option': option,
            'zone': zone,
        }
        return render(request, "lead/editlead.html", context)

    def post(self, request, id):
        outlet = request.POST['outlet']
        if not outlet:
            messages.error(request, 'Outlet Required')
            return redirect('/leads/')
        z = request.POST['zone']
        zone = Zone.objects.get(zone=z)
        owner = request.POST['owner']
        contact = request.POST['contact']
        coordinates = request.POST['coordinates']
        time = request.POST['timings']
        address = request.POST['address']
        option = request.POST['option']
        status = Status.objects.get(option=option)
        lead = Leads.objects.get(id=id)
        lead.author = request.user
        lead.outlet = outlet
        lead.zone = zone
        lead.owner = owner
        lead.contact = contact
        lead.address = address
        lead.status = status
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


class DeleteView(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def get(self, request):
        lead = Leads.objects.filter(author=request.user).order_by('-date')
        try:
            o = request.GET['option']
            status = Status.objects.get(option=o)
            lead = lead.filter(status=status.id)
        except:
            status = Status.objects.all()
        try:
            z = request.GET['zone']
            zone = Zone.objects.get(zone=z)
            lead = lead.filter(zone=zone.id)
        except:
            zone = Zone.objects.all()
        try:
            date_min = request.GET['min-date']
            date_max = request.GET['max-date']
            lead = lead.filter(date__gte=date_min)
            lead = lead.filter(date__lte=date_max)
        except:
            print('ok')
        context = {
            'lead': lead,
            'option': Status.objects.all(),
            'zone': Zone.objects.all(),
        }
        return render(request, "lead/delete.html", context)

    def post(self, request):
        items = request.POST.getlist('delitem')
        print(items)
        for i in items:
            lead = Leads.objects.get(id=int(i))
            lead.delete()
        return redirect("/search-delete/")