from rest_framework import routers
from visitor.viewsets import VisitorProfileViewSet, VisitViewSet, VisitAnalyticsViewSet, DatewiseVisitor

router = routers.DefaultRouter()
router.register("profile", VisitorProfileViewSet, basename="visitor-profile")
router.register("visits", VisitViewSet, basename="visit")
router.register("dateWisefilter", DatewiseVisitor, basename="date-wise-visitor")
router.register("analytics", VisitAnalyticsViewSet, basename="visit-analytics")

urlpatterns = router.urls
