from rest_framework import serializers
from .models import *
from django.utils import timezone

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Employee
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    checked_out_by = EmployeeSerializer()
    class Meta:
        model = Device
        fields = '__all__'

class DeviceCheckoutReturnedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['checked_out_by','checked_out_date','latest_condition','returned_date','is_available']
    
    def validate(self, attrs):
        device_id = self.context['device_id']
        action = self.context['action']
        device = Device.objects.get(id = device_id)
        # if [action] is checkout then we will check whether the device is available for checkout or not
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
        # if the [action] is checkout then
        # the checkout time will be present time and retured_data will be set to None,
        # as the device isn't returned yet
        # and we are setting the device log when it's checkouting
        # else the time of returning we are setting,
        # checked_out_date,checked_out_by to None and availability to True
        # and device log check_in with the returned condition 
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