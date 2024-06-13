from django.contrib import admin
from django.urls import path
from visitor import views

urlpatterns = [
    path(
        "visitor-register/",
        views.create_visitor_and_visit,
        name="visitor-register",
    ),
    path(
        "visitor-details/",
        views.fetch_visitor_details,
        name="visitor-details",
    ),
    path(
        "visitor-log/",
        views.visitor_data_with_visit_details,
        name="visitor-log",
    ),
    path(
        "datewise-visitor/",
        views.fetch_visitor_details_by_date,
        name="datewise-visitor",
    ),
    path(
        "daterange-wise-visitor/",
        views.fetch_visitor_details_by_date_range,
        name="daterange-wise-visitor",
    ),
    path(
        "most_visited_employee_details/",
        views.most_visited_employee_details,
        name="most_visited_employee_details",
    ),
    path(
        "visitor-email-notification/",
        views.send_visitor_notification_email,
        name="visitor-email-notification",
    ),
    path("send-django-email/", views.send_django_email, name="send-django-email"),
    path(
        "datewise-total-visitor/",
        views.total_visitors_by_date,
        name="datewise-total-visitor",
    ),
    path(
        "daterange-wise-total-visitor/",
        views.total_visitors_by_date_range,
        name="daterange-wise-total-visitor",
    ),
    path("download-visitor-report/", views.downaload_visitor_report, name="download-visitor-report"),
    path(
        "visitor-analytics/",
        views.visitor_analytics,
        name="visitor-analytics",
    ),
    path(
        "weekly-visitor-count/", views.weekly_visitor_count, name="weekly_visitor_count"
    ),
    path("visit-purpose-graph/", views.visit_purpose_graph, name="visit_purpose_graph"),
    path(
        "update-visitor/<uuid:visit_id>/", views.update_visitor, name="update_visitor"
    ),
    path(
        "gate/<int:gate_id>/visitor_form/",
        views.visitor_self_registration,
        name="visitor_form",
    ),
    path(
        "gate/<int:gate_id>/visitor_registration/",
        views.visitor_registration,
        name="visitor_registration",
    ),

    # path('new_visit_registration/<int:gate_id>/', views.new_visit_registration, name='new_visit_registration'),

    path("get-visitor-profile/", views.get_visitor_profile, name="get_visitor_profile"),
    path(
        "submit-visit-details/", views.submit_visit_details, name="submit_visit_details"
    ),
    path(
        "submit-self-visit-details/",
        views.submit_self_visit_details,
        name="submit_self_visit_details",
    ),
]
