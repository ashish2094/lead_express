from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.
class Status(models.Model):
    option = models.CharField(max_length=100, default="None")

    def __str__(self):
        return str(self.option)


class Zone(models.Model):
    zone = models.CharField(max_length=100, default="None")

    def __str__(self):
        return str(self.zone)


class Leads(models.Model):
    date = models.DateField(default=now)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    outlet = models.CharField(max_length=100, default="New")
    zone = models.ForeignKey(to=Zone, null=True, on_delete=models.SET_NULL)
    coordinates = models.CharField(max_length=100, default="None")
    timings = models.CharField(max_length=100, default="None")
    address = models.TextField(null=True)
    status = models.ForeignKey(to=Status, null=True, on_delete=models.SET_NULL)
    owner = models.CharField(max_length=100, default="None")
    contact = models.CharField(max_length=100, default="None")

    def __str__(self):
        return str(self.outlet)

    class Meta:
        ordering: ['-date']