from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
# Create your views here.

class CompanyViewset(ModelViewSet):
    serializer_class = CompanySerializer
    http_method_names = ['get','post']

    # this queryset if anyone hit the endpoint without his company name
    # he will get empty list, and with company name he will get his company details.
    def get_queryset(self):
        try:
            queryset = Company.objects.filter(name = self.request.data['name'])
        except:
            queryset = []
        return queryset

class EmployeeViewset(ModelViewSet):
    serializer_class = EmployeeSerializer
    http_method_names = ['get','post']

    def get_queryset(self):
        company_name = self.request.data['company']
        company = Company.objects.get(name = company_name)
        return Employee.objects.filter(company = company)

class DeviceViewset(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return DeviceCheckoutReturnedSerializer
        return DeviceSerializer

    def get_queryset(self):
        queryset =  Device.objects.all()
        if self.request.method == "GET":
            company_name = self.request.data['company']
            company = Company.objects.get(name = company_name)
            queryset = queryset.filter(company= company)
        return queryset
    
    def get_serializer_context(self):
         # here we are taking the action parameter from request body
         # [action] denotes whether any device is checkouting or returning
         context_data = {}
         if self.request.method == "PATCH":
            try:
                context_data['action'] = self.request.data['action']
                context_data['device_id']  = self.kwargs['pk']
            except Exception as e:
                print(e)
         return context_data
    

class DeviceLogViewset(ModelViewSet):
    serializer_class = DeviceLogSerializer
    http_method_names = ['get']

    # this queryset if anyone hit the endpoint without his company name
    # he will get empty list, and with company name he will get his company details.
    def get_queryset(self):
        print(self.request.data)
        queryset =  DeviceLog.objects.all()
        if self.request.method == "GET":
            company_name = self.request.data['company']
            company = Company.objects.get(name = company_name)
            device = Device.objects.filter(company = company)
            queryset = queryset.filter(device__in= device)
        return queryset

def payment_gateway(request):
    # first we will need to create a API key or Secret key of the third party payment integration company
    # then using that API key or API credentials we will develop integration code in this method which will take
    # User payment related informations like credit-card info,CVV, phon number , address etc.
    # Then after calling this function payment details of user will securely transmitted to the payment gateway or processor using this integration code.
    # the payment-gateway will verify the details with CVV and the bank infos and pay to the targeted account and give a success or error response.
    print("Placeholder of payment gateway integration")