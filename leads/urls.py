from django.urls import path
from .views import LeadView, LeadAddView, Exportxl, Importxl, EditLeadView, DeleteLeadView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('leads/', LeadView.as_view(), name='lead-dashboard'),
    path('lead-add/', LeadAddView.as_view(), name='lead-add'),
    path('lead_edit/<id>/', EditLeadView.as_view(), name='lead-edit'),
    path('lead_delete/<id>/', DeleteLeadView.as_view(), name='lead-delete'),
    path('export-excel/', Exportxl.as_view(), name='export-xl'),
    path('import-excel/', Importxl.as_view(), name='import-xl'),
]