from django.db import models
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)

class Device(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    device_model = models.CharField(max_length=100)
    checked_out_by = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL, related_name='checked_out_devices')
    checked_out_date = models.DateTimeField(null=True, blank=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    latest_condition = models.TextField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    # Add any other fields relevant to a device, such as serial number, model, etc.


class DeviceLog(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='logs')
    checked_out_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    checkout_condition = models.TextField()
    returned_condition = models.TextField()
    checked_out_date =  models.DateTimeField(null=True, blank=True)
    returned_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.device.name
    
    def check_out(self, employee, checkout_condition):
        self.checked_out_by = employee
        self.checkout_condition = checkout_condition
        self.checked_out_date = timezone.now()
        self.save()

    def check_in(self, returned_condition):
        self.checked_out_by = None
        self.checked_out_date = None
        self.returned_condition = returned_condition
        self.returned_date = timezone.now()
        self.save()