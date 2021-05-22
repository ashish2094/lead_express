from django.contrib import admin
from .models import Leads, Status, Zone
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class MetaAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'outlet', 'zone', 'coordinates', 'timings',
                    'address', 'status', 'date')
    search_fields = ('outlet', 'zone', 'coordinates', 'timings', 'address',
                     'status')


class MetaStatus(ImportExportModelAdmin):
    list_display = ('id', 'option')


class MetaZone(ImportExportModelAdmin):
    list_display = ('id', 'zone')


admin.site.register(Leads, MetaAdmin)
admin.site.register(Status, MetaStatus)
admin.site.register(Zone, MetaZone)
