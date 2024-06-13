from django.contrib import admin
from visitor.models import VisitorProfile, Visit
from import_export.admin import ImportExportModelAdmin


class VisitorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = VisitorProfile
    list_display = (
        "first_name",
        "last_name",
        "mobile_number",
        "address",
        "gender",
    )
    list_filter = (
        "email",
        "mobile_number",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
        "mobile_number",
    )
    ordering = ("id",)


admin.site.register(VisitorProfile, VisitorAdmin)


class VisitAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = Visit
    list_display = (
        "id",
        "no_of_individuals",
        "purpose",
        "check_in",
        "check_out",
        "is_active",
        "visitor",
        "gate",
        "employee",
    )
    list_filter = (
        "check_in",
        "check_out",
        "visitor",
    )
    search_fields = (
        "visitor__first_name",
        "visitor__last_name",
    )
    ordering = ("id",)


admin.site.register(Visit, VisitAdmin)
