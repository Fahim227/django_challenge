from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from rest_framework import generics, mixins, views
from .models import *
from .serializers import *
# Create your views here.

class CompanyViewset(ModelViewSet):
    serializer_class = CompanySerializer
    http_method_names = ['get','post']

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

"""mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet"""
class DeviceViewset(ModelViewSet):
    # queryset = Device.objects.all(company = company)
    # serializer_class = DeviceSerializer
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
         
         context_data = {}
         if self.request.method == "PATCH":
            try:
                context_data['action'] = self.request.data['action']
                context_data['device_id']  = self.kwargs['pk']
            except Exception as e:
                print(e)
         return context_data
    
    # def update(self, request, *args, **kwargs):
    #     try:
    #         print(self.request.data['action'])
    #     return super().update(request, *args, **kwargs)
    


