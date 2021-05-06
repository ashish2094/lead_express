from django.urls import path
from .views import LeadView, LeadAddView, Exportxl, Importxl
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('leads/', LeadView.as_view(), name='lead-dashboard'),
    path('lead-add/', LeadAddView.as_view(), name='lead-add'),
    path('export-excel/', Exportxl.as_view(), name='export-xl'),
    path('import-excel/', Importxl.as_view(), name='import-xl'),
]