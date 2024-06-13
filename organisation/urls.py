from django.contrib import admin
from django.urls import path
from organisation import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("employee-register/", views.create_employee_profile, name="employee_register"),
    path("show-department/", views.show_department, name="show-department"),
    path("add-department/", views.add_department, name="add-department"),
    path("employee-list/", views.employee_list, name="employee-list"),
    path("add-unit/", views.add_unit, name="add-unit"),
    path("unit-list/", views.unit_list, name="unit-list"),
    path("add-gate/", views.add_gate, name="add-gate"),
    path("gate-list/", views.gate_list, name="gate-list"),
    path("update-gate/<int:gate_id>/", views.update_gate, name="update-gate"),
    path("update-unit/<uuid:unit_id>/", views.update_unit, name="update-unit"),
    path(
        "update-department/<uuid:dept_id>/",
        views.update_department,
        name="update-department",
    ),
    path(
        "update-employee/<uuid:emp_id>/", views.update_employee, name="update-employee"
    ),
    path(
        "deactivate-department/<uuid:dept_id>/",
        views.deactivate_department,
        name="deactivate_department",
    ),
    path(
        "deactivate-unit/<uuid:unit_id>/", views.deactivate_unit, name="deactivate_unit"
    ),
    path(
        "deactivate-gate/<int:gate_id>/", views.deactivate_gate, name="deactivate_gate"
    ),
    path(
        "deactivate-employee/<uuid:emp_id>/",
        views.deactivate_employee,
        name="deactivate_employee",
    ),
    path('gen_qr/<int:gate_id>/', views.gate_qrcard, name='gen_qr'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
