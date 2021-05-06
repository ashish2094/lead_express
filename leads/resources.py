from import_export import resources
from .models import Leads

class LeadResource(resources.ModelResource):
    class meta:
        model = Leads