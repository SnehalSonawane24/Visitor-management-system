from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from organisation.models import Department, EmployeeProfile, Gate, Organisation, Unit
from visitor.views import generate_qr_code, organisations_details
from organisation.forms import (
    DepartmentForm,
    EmployeeProfileForm,
    GateForm,
    UnitForm,
    UpdateDepartmentForm,
    UpdateEmployeeProfileForm,
    UpdateGateForm,
    UpdateUnitForm,
)


def get_paginated_data(data, request, per_page):
    """
    Helper function to paginate data
    """
    paginator = Paginator(data, per_page)
    page_number = request.GET.get("page")

    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_data = paginator.page(1)
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)

    return paginated_data


def add_unit(request):
    """
    Function for adding unit
    """
    if request.method == "POST":
        if request.user.is_authenticated:
            creator = request.user
            updater = request.user
            unit_fm = UnitForm(request.user, request.POST)
        else:
            return render(request, "visitor/authentication_required.html")

    unit_fm = UnitForm(request.user, request.POST)

    if unit_fm.is_valid():
        unit_data = unit_fm.cleaned_data
        name = unit_data["name"]
        address = unit_data["address"]
        description = unit_data["description"]
        org = unit_data["org"]
        unit = Unit.objects.create(
            name=name,
            address=address,
            description=description,
            org=org,
            created_by=creator,
            updated_by=updater,
        )
        return render(request, "organisation/unit_thank_you.html")

    else:
        unit_fm = UnitForm(request.user, request.POST)

    return render(request, "organisation/add_unit.html", {"unit_form": unit_fm})


def unit_list(request):
    """
    Function for fetching all unit list
    """
    user = request.user
    _, organisation_names, units_in_organisations = organisations_details(user)

    paginated_units = get_paginated_data(units_in_organisations, request, per_page=5)
    return render(
        request,
        "organisation/unit_list.html",
        {
            "units": paginated_units,
            "organisation_names": organisation_names,
        },
    )


def update_unit(request, unit_id):
    """
    Function for update unit details
    """
    user = request.user
    unit = get_object_or_404(Unit, id=unit_id)
    _, organisation_names, units_in_organisations = organisations_details(user)
    if request.method == "POST":
        form = UpdateUnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect("unit-list")
    else:
        form = UpdateUnitForm(instance=unit)

    return render(
        request,
        "organisation/update_unit.html",
        {
            "form": form,
            "unit": unit,
            "organisation_names": organisation_names,
        },
    )


@csrf_exempt
def deactivate_unit(request, unit_id):
    """
    Deactivate a unit by setting is_active to False
    """
    unit = get_object_or_404(Unit, id=unit_id)
    unit.deactivate_unit()
    return redirect("/organisation/unit-list/")


def add_department(request):
    """
    Function for adding a department
    """
    if request.method == "POST":
        creator = request.user
        updater = request.user
        department_fm = DepartmentForm(request.user, request.POST)

        if department_fm.is_valid():
            dept_data = department_fm.cleaned_data
            name = dept_data["name"]
            department_type = dept_data["department_type"]
            org = dept_data["org"]
            unit = dept_data["unit"]

            department = Department.objects.create(
                name=name,
                department_type=department_type,
                org=org,
                unit=unit,
                created_by=creator,
                updated_by=updater,
            )
            return render(request, "visitor/department_thank_you.html")

    else:
        department_fm = DepartmentForm(user=request.user)

    return render(
        request, "organisation/add_department.html", {"department_form": department_fm}
    )


def show_department(request):
    """
    Function for fetching all department list
    """
    user = request.user
    organisations, organisation_names, _ = organisations_details(user)
    departments = (
        Department.objects.select_related("org")
        .prefetch_related("dept_emp__permissions__user_acc")
        .filter(org__in=organisations)
    )

    departments_paginated = get_paginated_data(departments, request, per_page=5)

    return render(
        request,
        "organisation/department.html",
        {
            "departments": departments_paginated,
            "organisation_names": organisation_names,
        },
    )


def update_department(request, dept_id):
    """
    Function for department department details
    """
    user = request.user
    department = get_object_or_404(Department, id=dept_id)
    _, organisation_names, units_in_organisations = organisations_details(user)

    if request.method == "POST":
        form = UpdateDepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect("show-department")
    else:
        form = UpdateDepartmentForm(instance=department)

    return render(
        request,
        "organisation/update_department.html",
        {
            "form": form,
            "department": department,
            "unit": units_in_organisations,
            "organisation_names": organisation_names,
        },
    )


@csrf_exempt
def deactivate_department(request, dept_id):
    """
    Deactivate a department by setting is_active to False
    """
    department = get_object_or_404(Department, id=dept_id)
    department.deactivate_department()
    return redirect("/organisation/show-department/")


def add_gate(request):
    """
    Function for adding gate
    """
    if request.method == "POST":
        if request.user.is_authenticated:
            creator = request.user
            updater = request.user
            gate_fm = GateForm(request.user, request.POST)

        else:
            return render(request, "visitor/authentication_required.html")

    gate_fm = GateForm(request.user, request.POST)

    if gate_fm.is_valid():
        gate_data = gate_fm.cleaned_data
        name = gate_data["name"]
        description = gate_data["description"]
        unit = gate_data["unit"]
        gate = Gate.objects.create(
            name=name,
            description=description,
            unit=unit,
            created_by=creator,
            updated_by=updater,
        )
        return render(request, "organisation/gate_thank_you.html")

    else:
        gate_fm = GateForm(request.user, request.POST)

    return render(request, "organisation/add_gate.html", {"gate_form": gate_fm})


def gate_list(request):
    """
    Function for fetching all gate list
    """
    user = request.user
    organisations, organisation_names, _ = organisations_details(user)
    units = Unit.objects.filter(org__in=organisations)
    gates = Gate.objects.filter(unit__in=units)
    gates_paginated = get_paginated_data(gates, request, per_page=5)
    return render(
        request,
        "organisation/gate_list.html",
        {
            "gates": gates_paginated,
            "organisation_names": organisation_names,
        },
    )


def update_gate(request, gate_id):
    """
    Function for update gate details
    """
    user = request.user
    gate = get_object_or_404(Gate, id=gate_id)
    _, organisation_names, units_in_organisations = organisations_details(user)

    if request.method == "POST":
        form = UpdateGateForm(request.POST, instance=gate)
        if form.is_valid():
            form.save()
            return redirect("gate-list")
    else:
        form = UpdateGateForm(instance=gate)

    return render(
        request,
        "organisation/update_gate.html",
        {
            "form": form,
            "gate": gate,
            "units": units_in_organisations,
        },
    )


@csrf_exempt
def deactivate_gate(request, gate_id):
    """
    Deactivate a gate by setting is_active to False
    """
    gate = get_object_or_404(Gate, id=gate_id)
    gate.deactivate_gate()
    return redirect("/organisation/gate-list/")


def create_employee_profile(request):
    """
    Function for employee registration
    """
    if request.method == "POST":
        if request.user.is_authenticated:
            creator = request.user
            updater = request.user
            employee_fm = EmployeeProfileForm(
                request.user, request.POST, request.FILES
            )  # Pass request.user to DepartmentForm

        else:
            return render(request, "visitor/authentication_required.html")

        employee_fm = EmployeeProfileForm(
            request.user, request.POST, request.FILES
        )  # Pass request.user to DepartmentForm

        if employee_fm.is_valid():
            # Extract data from forms
            employee_data = employee_fm.cleaned_data
            first_name = employee_data["first_name"]
            middle_name = employee_data["middle_name"]
            last_name = employee_data["last_name"]
            email = employee_data["email"]
            mobile_number = employee_data["mobile_number"]
            gender = employee_data["gender"]
            marital_status = employee_data["marital_status"]
            photo = employee_data["photo"]
            address = employee_data["address"]
            department = employee_data["department"]
            date_of_birth = employee_data["date_of_birth"]

            # Check if a Employee Profile with the provided email or mobile number already exists
            if (
                EmployeeProfile.objects.filter(email=email).exists()
                or EmployeeProfile.objects.filter(mobile_number=mobile_number).exists()
            ):
                return HttpResponse(
                    "Employee with the provided email or mobile number already exists."
                )

            # If no existing profile found, create a new Employee Profile instance
            employee_profile = EmployeeProfile.objects.create(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                email=email,
                mobile_number=mobile_number,
                gender=gender,
                marital_status=marital_status,
                photo=photo,
                address=address,
                date_of_birth=date_of_birth,
                department=department,
                created_by=creator,
                updated_by=updater,
            )

            return render(
                request,
                "organisation/emp_thank_you.html",
                {"employee_profile": employee_profile},
            )
    else:
        employee_fm = EmployeeProfileForm(
            request.user, request.POST, request.FILES
        )  # Pass request.user to DepartmentForm
    return render(
        request, "organisation/employee_register.html", {"employee_form": employee_fm}
    )


def employee_list(request):
    """
    Function for fetching all employee list
    """
    user = request.user
    organisations, organisation_names, _ = organisations_details(user)
    employees = EmployeeProfile.objects.select_related("department").filter(
        department__org__in=organisations
    )
    # organisation_names = get_organisation_names(request)

    employees_paginated = get_paginated_data(employees, request, per_page=5)

    return render(
        request,
        "organisation/employee_list.html",
        {
            "employees": employees_paginated,
            "organisation_names": organisation_names,
        },
    )


def update_employee(request, emp_id):
    """
    Function to update employee details
    """
    employee = get_object_or_404(EmployeeProfile, id=emp_id)
    if request.method == "POST":
        form = UpdateEmployeeProfileForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect("employee-list")
        
    else:
        form = UpdateEmployeeProfileForm(instance=employee)

    return render(
        request,
        "organisation/update_employee.html",
        {"form": form, "employee": employee},
    )


@csrf_exempt
def deactivate_employee(request, emp_id):
    """
    Deactivate a employee by setting is_active to False
    """
    employee = get_object_or_404(EmployeeProfile, id=emp_id)
    employee.deactivate_employee()
    return redirect("/organisation/employee-list/")


def gate_qrcard(request, gate_id):
    gate = get_object_or_404(Gate, id=gate_id)
    gate_name = gate.name
    unit_name = gate.unit.name
    organisations_details = gate.unit.org.name

    base_url = request.build_absolute_uri("/")
    visitor_url = (
        f"{base_url}visitor/gate/{gate_id}/visitor_form/"
    )

    # Generate QR Code
    qr_code_url = generate_qr_code(visitor_url, f"qr_code_{gate_id}.png")

    return render(
        request,
        "organisation/qr_code.html",
        {
            "gate": gate,
            "unit_name": unit_name,
            "organisations_details": organisations_details,
            "qr_code_url": qr_code_url,
        },
    )
