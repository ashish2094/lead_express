from import_export import resources
from import_export.fields import Field
from .models import Leads

class LeadResource(resources.ModelResource):
    sr = Field(column_name='Sr.No.')
    class meta:
        model = Leads
        
        fields = ('outlet', 'zone', 'coordinates', 'timings', 'address', 'remark', 'date')
        export_order = ('outlet', 'zone', 'coordinates', 'timings', 'address', 'remark', 'date')