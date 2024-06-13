from django import forms
from visitor.models import VisitorProfile, Visit
from organisation.models import EmployeeProfile, Gate, Organisation, Unit
from django.utils import timezone

class VisitorProfileForm(forms.ModelForm):
    full_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={"class": "form-control"}))
    class Meta:
        model = VisitorProfile
        fields = [
            "full_name",
            "email",
            "mobile_number",
            "photo",
            "address",
        ]

        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "required": False}),
            "mobile_number": forms.TextInput(attrs={"class": "form-control", "required": False}),
            "photo": forms.FileInput(attrs={"required": False}),
            "address": forms.TextInput(attrs={"class": "form-control", "required":False}),
        }

class VisitForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(VisitForm, self).__init__(*args, **kwargs)
        if user and hasattr(user, "is_authenticated") and user.is_authenticated:
            organisations = Organisation.objects.filter(
                dept_org__dept_emp__permissions__user_acc=user
            )

            # Filter employees by organization
            employees = EmployeeProfile.objects.select_related("department").filter(
                department__org__in=organisations
            )
            self.fields["employee"].queryset = employees

            # Filter gates by organization
            units = Unit.objects.filter(org__in=organisations)
            gates = Gate.objects.filter(unit__in=units)
            self.fields["gate"].queryset = gates

            self.initial["check_in"] = timezone.localtime(timezone.now()).strftime(
                "%Y-%m-%dT%H:%M"
            )

    class Meta:
        model = Visit
        fields = [
            "no_of_individuals",
            "purpose",
            "check_out",
            "vehicle_number",
            "employee",
            "gate",
        ]

        widgets = {
            "purpose": forms.TextInput(attrs={"class": "form-control"}),
            "check_out": forms.HiddenInput(attrs={"required": False}),
            "vehicle_number": forms.TextInput(attrs={"class": "form-control", "required": False}),
            "no_of_individuals": forms.NumberInput(attrs={"class": "form-control"}),
            "employee": forms.Select(attrs={"class": "form-control", "required": False}),
            "gate": forms.Select(attrs={"class": "form-control", "required": False}),
        }


class UpdateVisitorForm(forms.ModelForm):
    class Meta:
        model = VisitorProfile
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "mobile_number",
            "address",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "middle_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "mobile_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
        }


class UpdateVisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = [
            "purpose",
            "check_in",
            "no_of_individuals",
            "employee",
            "gate",
        ]

        widgets = {
            "purpose": forms.TextInput(attrs={"class": "form-control"}),
            "no_of_individuals": forms.NumberInput(attrs={"class": "form-control"}),
            "check_in": forms.DateTimeInput(attrs={"class": "form-control"}),
            "employee": forms.Select(attrs={"class": "form-control"}),
            "gate": forms.Select(attrs={"class": "form-control"}),
        }
