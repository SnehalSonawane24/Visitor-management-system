from datetime import datetime
from rest_framework import viewsets, filters
from visitor.models import VisitorProfile, Visit
from visitor.serializers import VisitorProfileSerializer, VisitSerializer
from visitor.views import organisations_details
from django.db.models import Q, Count
from datetime import datetime, timedelta
from rest_framework.response import Response
from django.utils import timezone


class VisitorProfileViewSet(viewsets.ModelViewSet):
    serializer_class = VisitorProfileSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ["email", "mobile_number", "first_name", "last_name"]

    ordering_fields = ["created_at", "updated_at"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            _, _, units_in_organisations = organisations_details(user)
            return VisitorProfile.objects.filter(
                visit_visitor__gate__unit__in=units_in_organisations
            )
        return VisitorProfile.objects.none()


class VisitViewSet(viewsets.ModelViewSet):
    serializer_class = VisitSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ["purpose"]

    ordering_fields = ["check_in", "check_out", "created_at", "updated_at"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            _, _, units_in_organisations = organisations_details(user)
            return Visit.objects.filter(
                visitor__visit_visitor__gate__unit__in=units_in_organisations
            )
        return Visit.objects.none()


class DatewiseVisitor(viewsets.ModelViewSet):
    serializer_class = VisitSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            date_str = self.request.query_params.get("date")
            if date_str:
                try:
                    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    return Visit.objects.none()

                _, _, units_in_organisations = organisations_details(user)
                return Visit.objects.filter(
                    visitor__visit_visitor__gate__unit__in=units_in_organisations,
                    check_in__date=target_date,
                )

        return Visit.objects.none()


class VisitAnalyticsViewSet(viewsets.ViewSet):
    def get_visitors_count(
        self, units_in_organisations, start_date=None, end_date=None
    ):
        query = Visit.objects.filter(gate__unit__in=units_in_organisations)
        if start_date and end_date:
            query = query.filter(check_in__date__range=[start_date, end_date])
        elif start_date:
            query = query.filter(check_in__date__gte=start_date)
        return query.count()

    def list(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            _, _, units_in_organisations = organisations_details(user)

            today = timezone.now().date()
            yesterday = today - timedelta(days=1)
            week_start = today - timedelta(days=today.weekday())
            month_start = datetime(today.year, today.month, 1)
            year_start = datetime(today.year, 1, 1)

            date_ranges = {
                "todays_visitors_count": (today, today),
                "yesterdays_visitors_count": (yesterday, yesterday),
                "weekly_visitors_count": (week_start, today),
                "monthly_visitors_count": (month_start, today),
                "yearly_visitors_count": (year_start, today),
            }

            visitors_counts = {
                label: self.get_visitors_count(units_in_organisations, start, end)
                for label, (start, end) in date_ranges.items()
            }

            overall_visitors_count = Visit.objects.filter(
                gate__unit__in=units_in_organisations
            ).count()

            most_visited_purpose_details = (
                Visit.objects.filter(gate__unit__in=units_in_organisations)
                .values("purpose")
                .annotate(visit_count=Count("purpose"))
                .order_by("-visit_count")
                .first()
            )
            most_visited_employee_id = (
                Visit.objects.filter(gate__unit__in=units_in_organisations)
                .values("id")
                .annotate(visit_count=Count("employee"))
                .order_by("-visit_count")
                .first()
            )

            data = {
                **visitors_counts,
                "overall_visitors_count": overall_visitors_count,
                "most_visited_purpose_details": most_visited_purpose_details,
                "most_visited_employee_details": most_visited_employee_id,
            }

            return Response(data)
