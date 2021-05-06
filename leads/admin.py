from django.contrib import admin
from .models import Leads
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class MetaAdmin(ImportExportModelAdmin):
    list_display = ('id','author','outlet', 'zone', 'coordinates', 'timings', 'address', 'remark', 'date')
    search_fields = ('outlet', 'zone', 'coordinates', 'timings', 'address', 'remark')

admin.site.register(Leads, MetaAdmin)
