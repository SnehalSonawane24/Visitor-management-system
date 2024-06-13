from rest_framework import routers
from organisation.viewsets import (
    OrganisationViewSet,
    UnitViewSet,
    GateViewSet,
    DepartmentViewSet,
    EmployeeProfileViewSet,
    EmployeeAuthorizationViewSet,
)

router = routers.DefaultRouter()

router.register("organisations", OrganisationViewSet, basename="organisation")
router.register("units", UnitViewSet, basename="unit")
router.register("gates", GateViewSet, basename="gate")
router.register("department", DepartmentViewSet, basename="department")
router.register("employee", EmployeeProfileViewSet, basename="employee-profile")
router.register(
    "employee-authorizations",
    EmployeeAuthorizationViewSet,
    basename="employee-authorization",
)

urlpatterns = router.urls
