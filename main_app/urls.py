from rest_framework import routers
from main_app import views


router = routers.DefaultRouter()

router.register('company',views.CompanyViewset,basename="company")
router.register('employee',views.EmployeeViewset,basename="employee")
router.register('device',views.DeviceViewset,basename="device")

urlpatterns = router.urls