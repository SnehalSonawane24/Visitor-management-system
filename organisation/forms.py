from django import forms
from organisation.models import EmployeeProfile, Department, Organisation, Unit, Gate
from visitor.views import organisations_details

class EmployeeProfileForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(EmployeeProfileForm, self).__init__(*args, **kwargs)
        organisations, _, _ = organisations_details(user)
        departments = Department.objects.select_related("org").filter(
            org__in=organisations
        )
        self.fields["department"].queryset = departments

    class Meta:
        model = EmployeeProfile
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "mobile_number",
            "gender",
            "photo",
            "address",
            "date_of_birth",
            "marital_status",
            "department",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "middle_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "mobile_number": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "photo": forms.FileInput(),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_birth": forms.HiddenInput(attrs={"class": "form-control"}),
            "marital_status": forms.Select(attrs={"class": "form-control"}),
            "department": forms.Select(attrs={"class": "form-control"}),
        }
 
class DepartmentForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        organisations, _, _ = organisations_details(user)
        self.fields["org"].queryset = organisations
        # Filter units by their associated organisation
        units = Unit.objects.filter(org__in=organisations)
        self.fields["unit"].queryset = units

    class Meta:
        model = Department
        fields = ["name", "department_type", "org", "unit"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "department_type": forms.TextInput(attrs={"class": "form-control"}),
            "org": forms.Select(attrs={"class": "form-control"}),
            "unit": forms.Select(attrs={"class": "form-control"}),
        }

        labels = {
            "name": "Department Name",
            "org": "Organisation",
            "department_type": "Department Type",
            "unit": "Branch",
        }


class UnitForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)
        organisations, _, _ = organisations_details(user)
        self.fields["org"].queryset = organisations

    class Meta:
        model = Unit
        fields = ["name", "address", "description", "org"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "org": forms.Select(attrs={"class": "form-control"}),
        }

        labels = {
            "name": "Unit Name",
            "address": "Address",
            "description": "Description",
            "org": "Organisation",
        }


class GateForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(GateForm, self).__init__(*args, **kwargs)
        organisations, _, _ = organisations_details(user)
        units = Unit.objects.filter(org__in=organisations)
        self.fields["unit"].queryset = units

    class Meta:
        model = Gate
        fields = ["name", "description", "unit"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "unit": forms.Select(attrs={"class": "form-control"}),
        }

        labels = {
            "name": "Gate Name",
            "description": "Purpose",
            "unit": "Unit",
        }

class UpdateGateForm(forms.ModelForm):
    class Meta:
        model = Gate
        fields = ["name", "description", "unit"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "unit": forms.Select(attrs={"class": "form-control"}),
        }

        labels = {
            "name": "Gate Name",
            "description": "Purpose",
            "unit": "Unit",
        }


class UpdateUnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ["name", "address", "description", "org"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "org": forms.Select(attrs={"class": "form-control"}),
        }

        labels = {
            "name": "Unit Name",
            "address": "Address",
            "description": "Description",
            "org": "Organisation",
        }


class UpdateDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "department_type", "org", "unit"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "department_type": forms.TextInput(attrs={"class": "form-control"}),
            "org": forms.Select(attrs={"class": "form-control"}),
            "unit": forms.Select(attrs={"class": "form-control"}),
        }

        labels = {
            "name": "Department Name",
            "org": "Organisation",
            "department_type": "Department Type",
            "unit": "Branch",
        }


class UpdateEmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "mobile_number",
            "gender",
            "photo",
            "address",
            "date_of_birth",
            "marital_status",
            "department",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "middle_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "mobile_number": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "photo": forms.FileInput(),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_birth": forms.HiddenInput(attrs={"class": "form-control"}),
            "marital_status": forms.Select(attrs={"class": "form-control"}),
            "department": forms.Select(attrs={"class": "form-control"}),
        }