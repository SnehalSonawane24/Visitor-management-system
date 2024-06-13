from accounts.viewsets import UserAccountViewSet, StaffViewSet, ManagerViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register("user", UserAccountViewSet, basename="user")
router.register(r"staff", StaffViewSet, basename="staff")
router.register(r"manager", ManagerViewSet, basename="managers")

urlpatterns = router.urls
