from rest_framework import routers
# from django.urls import include, re_path

from main_app import views
# from rest_framework_swagger.views import get_swagger_view

# schema_view = get_swagger_view(title='Pastebin API')



router = routers.DefaultRouter()

router.register('company',views.CompanyViewset,basename="company")
router.register('employee',views.EmployeeViewset,basename="employee")
router.register('device',views.DeviceViewset,basename="device")
router.register('device_log',views.DeviceLogViewset,basename="device_log")

urlpatterns = router.urls
# urlpatterns.append(re_path(r'^$', schema_view)) 