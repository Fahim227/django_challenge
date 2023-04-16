from rest_framework import serializers
from .models import *
from django.utils import timezone

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class DeviceCheckoutReturnedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['checked_out_by','checked_out_date','latest_condition','returned_date','is_available']
    
    def validate(self, attrs):
        print("validate=============")
        device_id = self.context['device_id']
        action = self.context['action']
        device = Device.objects.get(id = device_id)
        if action.lower() == 'checkout':
            if device.is_available == False:
                raise  serializers.ValidationError("The Device is not available")
        return super().validate(attrs)

    def update(self, instance, validated_data):
        # get extra attribute from request body which will define whether
        # user wants to checkout or return opertaion
        action = self.context['action']
        device_id = self.context['device_id']
        device = Device.objects.get(id = device_id)
        
        if action.lower() == 'checkout':
            validated_data['checked_out_date'] = timezone.now() 
            validated_data['returned_date'] = None 
            validated_data['is_available'] = False 
            employee = validated_data['checked_out_by']
            device_log = DeviceLog(device = device)
            device_log.check_out(employee=employee,checkout_condition=validated_data['latest_condition'])
        elif action.lower() == 'return':
            validated_data['returned_date'] = timezone.now() 
            validated_data['checked_out_date'] = None
            validated_data['checked_out_by'] = None
            validated_data['is_available'] = True 
            device_log = DeviceLog(device = device)
            device_log.check_in(returned_condition=validated_data['latest_condition'])
        return super().update(instance, validated_data)

    
class DeviceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceLog
        fields = '__all__'