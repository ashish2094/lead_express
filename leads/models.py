from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Leads(models.Model):
    date = models.DateField(default=now)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    outlet = models.CharField(max_length = 100, default="New")
    zone = models.CharField(max_length = 100, default="None")
    coordinates = models.CharField(max_length = 100, default="None")
    timings = models.CharField(max_length = 100, default="None")
    address = models.TextField(null=True)
    remark = models.CharField(max_length = 100, default="None")
    
    def __str__(self):
        return str(self.outlet)
    class Meta:
        ordering: ['-date']