from django.contrib import admin
from organisation.models import (
    Organisation,
    Unit,
    Gate,
    Department,
    EmployeeProfile,
    EmployeeAuthorization,
    UnitAccessAuthorization,
)

from import_export.admin import ImportExportModelAdmin


# Register your models here.
class OrganisationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = Organisation
    list_display = ("id", "name", "org_type", "is_active", "created_at", "updated_at")
    search_fields = ("name", "org_type")
    ordering = ("id",)
    list_filter = ("org_type", "is_active")


admin.site.register(Organisation, OrganisationAdmin)


class UnitAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = Unit
    list_display = ("name", "address", "is_active", "org", "created_at", "updated_at")
    search_fields = ("name", "org__name")
    ordering = ("name",)
    list_filter = (
        "org",
        "is_active",
    )


admin.site.register(Unit, UnitAdmin)


class GateAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = Gate
    list_display = (
        "id",
        "name",
        "description",
        "is_active",
        "unit",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "unit__name")
    ordering = ("name",)
    list_filter = ("unit",)


admin.site.register(Gate, GateAdmin)


class DepartmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = Department
    list_display = (
        "id",
        "name",
        "department_type",
        "is_active",
        "unit",
        "org",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "department_type", "org__name")
    ordering = ("id",)
    list_filter = ("department_type", "is_active", "org")


admin.site.register(Department, DepartmentAdmin)


class EmployeeProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = EmployeeProfile
    list_display = (
        "id",
        "is_active",
        "first_name",
        "last_name",
        "mobile_number",
        "email",
        "department",
        "employee_organisation",
        "created_at",
        "updated_at",
    )
    search_fields = ("first_name", "last_name", "mobile_number", "department__name")
    ordering = ("id",)
    list_filter = ("gender", "marital_status", "department")
    fields = [
        ("created_by", "updated_by", "is_active"),
        ("first_name", "middle_name", "last_name"),
        ("email", "mobile_number"),
        ("gender", "date_of_birth"),
        ("marital_status", "photo"),
        "address",
        "department",
    ]

    def employee_organisation(self, obj):
        return obj.department.org.name if obj.department.org else None

    employee_organisation.short_description = "Organisation"


admin.site.register(EmployeeProfile, EmployeeProfileAdmin)


class EmployeeAuthorizationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = EmployeeAuthorization
    list_display = ("employee", "user_acc", "created_at", "updated_at")
    search_fields = (
        "employee__first_name",
        "employee__last_name",
        "user_acc__username",
    )
    ordering = ("id",)
    list_filter = ("user_acc",)


admin.site.register(EmployeeAuthorization, EmployeeAuthorizationAdmin)

class UnitAccessAuthorizationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = EmployeeAuthorization
    list_display = ("unit", "user_acc", "created_at", "updated_at")
    search_fields = (
        "unit__name",
        "user_acc__username",
    )
    ordering = ("id",)
    list_filter = ("user_acc", "unit")


admin.site.register(UnitAccessAuthorization, UnitAccessAuthorizationAdmin)
