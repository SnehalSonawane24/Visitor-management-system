import io
import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import qrcode
from requests import request
from visitor.models import VisitorProfile, Visit
from organisation.models import EmployeeProfile, Department, Gate, Organisation, Unit
from django.db.models import Q
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from django.db.models import Count
from django.shortcuts import redirect
from visitor.forms import VisitorProfileForm, VisitForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
import datetime
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, redirect, render
from .forms import UpdateVisitorForm
from .models import Visit
from django.core.exceptions import ObjectDoesNotExist
import xlsxwriter
import json
import pytz
import calendar
import logging
from visitor.forms import VisitForm, VisitorProfileForm
from django.contrib import messages

# Configure the logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                _, organisation_names, _ = organisations_details(user)

                return redirect("home")
    else:
        form = AuthenticationForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
        },
    )


def logout_view(request):
    logout(request)
    return redirect("login")


def organisations_details(user):
    organisations = Organisation.objects.filter(
        dept_org__dept_emp__permissions__user_acc=user
    )
    organisation_names = [org.name for org in organisations]
    units_in_organisations = Unit.objects.filter(org__in=organisations)
    return organisations, organisation_names, units_in_organisations


@csrf_exempt
def home(request):
    """
    Function for fetch active, inactive visitor and today's visitor count
    """
    user = request.user
    _, organisation_names, units_in_organisations = organisations_details(user)
    active_visitors = (
        Visit.objects.select_related("gate")
        .filter(gate__unit__in=units_in_organisations)
        .filter(check_out__isnull=True)
    )
    inactive_visitors = (
        Visit.objects.select_related("gate")
        .filter(gate__unit__in=units_in_organisations)
        .filter(check_out__isnull=False)
    )

    # Pagination for active visitors
    active_visitors_paginator = Paginator(active_visitors, 5)
    active_page = request.GET.get("active_page")
    try:
        active_visitors_page = active_visitors_paginator.page(active_page)
    except PageNotAnInteger:
        active_visitors_page = active_visitors_paginator.page(1)
    except EmptyPage:
        active_visitors_page = active_visitors_paginator.page(
            active_visitors_paginator.num_pages
        )

    # Pagination for inactive visitors
    inactive_visitors_paginator = Paginator(inactive_visitors, 5)
    inactive_page = request.GET.get("inactive_page")
    try:
        inactive_visitors_page = inactive_visitors_paginator.page(inactive_page)
    except PageNotAnInteger:
        inactive_visitors_page = inactive_visitors_paginator.page(1)
    except EmptyPage:
        inactive_visitors_page = inactive_visitors_paginator.page(
            inactive_visitors_paginator.num_pages
        )

    return render(
        request,
        "home.html",
        {
            "active_visitors_page": active_visitors_page,
            "inactive_visitors_page": inactive_visitors_page,
            "organisation_names": organisation_names,
        },
    )


def split_full_name(full_name):
    """
    Split the full name into first name, middle name, and last name
    """
    name_parts = full_name.strip().split()
    middle_name = ""
    last_name = ""

    if len(name_parts) == 1:
        first_name = name_parts[0]
    elif len(name_parts) == 2:
        first_name, last_name = name_parts
    elif len(name_parts) == 3:
        first_name, middle_name, last_name = name_parts
    else:
        first_name = name_parts[0]
        middle_name = name_parts[1]
        last_name = " ".join(name_parts[2:])

    return first_name, middle_name, last_name

@csrf_exempt
def create_visitor_and_visit(request):
    """
    Function for storing visitor data with visit details
    """
    employees = EmployeeProfile.objects.all()
    if request.method == "POST":
        if request.user.is_authenticated:
            creator = request.user
            updater = request.user
        else:
            return render(request, "visitor/authentication_required.html")

        visitor_fm = VisitorProfileForm(request.POST, request.FILES)
        visit_fm = VisitForm(request.user, request.POST)

        if visitor_fm.is_valid() and visit_fm.is_valid():
            visitor_data = visitor_fm.cleaned_data

            full_name = visitor_data.get("full_name")
            first_name, middle_name, last_name = split_full_name(full_name)

            visitor_profile = VisitorProfile.objects.create(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                email=visitor_data.get("email", None),
                mobile_number=visitor_data.get("mobile_number", None),
                photo=visitor_data.get("photo", None),
                address=visitor_data.get("address", None),
                created_by=creator,
                updated_by=updater,
            )

            visit_data = visit_fm.cleaned_data
            visit = Visit.objects.create(
                purpose=visit_data.get("purpose", ""),
                check_in=visit_data.get("check_in", timezone.now()),
                check_out=visit_data.get("check_out", None),
                no_of_individuals=visit_data.get("no_of_individuals", 1),
                vehicle_number=visit_data.get("vehicle_number", None),
                employee=visit_data.get("employee", None),
                gate=visit_data.get("gate", None),
                visitor=visitor_profile,
                created_by=creator,
                updated_by=updater,
            )

            return render(request, "visitor/thank_you.html")
        else:
            logger.info("Visitor Form Errors: %s", visitor_fm.errors)
            logger.info("Visit Form Errors: %s", visit_fm.errors)

    else:
        visitor_fm = VisitorProfileForm()
        visit_fm = VisitForm(user=request.user)

    return render(
        request,
        "visitor/visitor_visit_form.html",
        {"visitor_form": visitor_fm, "visit_form": visit_fm, "employee": employees},
    )


def send_visitor_notification_email(visitor, employee, visit):
    """
    Email template rendering using mailgun
    """
    context = {"visitor": visitor, "visit": visit, "employee": employee}
    email_html_message = render_to_string(
        "visitor/visitor_notification_email.html", context
    )
    email_plaintext_message = strip_tags(email_html_message)

    # Prepare data for sending email
    subject = "Visitor Notification"
    to_email = employee.email

    try:
        send_mail(
            subject,
            email_plaintext_message,
            None,
            [to_email],
            html_message=email_html_message,
        )
        return {"success": True, "message": "Email sent successfully"}
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        return {"success": False, "message": "Email not sent"}


@csrf_exempt
def send_django_email(visitor, employee, visit):
    """
    Email template sending using django email feature
    """
    context = {"visitor": visitor, "visit": visit, "employee": employee}

    email_html_message = render_to_string(
        "visitor/visitor_notification_email.html", context
    )
    email_plaintext_message = strip_tags(email_html_message)
    subject = "Visitor Notification"
    email_from = "jadenik13@gmail.com"
    to_email = employee.email
    try:
        send_mail(
            subject,
            email_plaintext_message,
            email_from,
            [to_email],
            html_message=email_html_message,
        )
        return JsonResponse({"success": True, "message": "Email sent successfully"})
    except Exception as e:
        return JsonResponse(
            {"success": False, "message": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR
        )


# TODO:
# @csrf_exempt
# def send_django_email(visitor, employee, visit):
#     """
#     Email template sending using django email feature with logo
#     """
#     context = {"visitor": visitor, "visit": visit, "employee": employee}

#     email_html_message = render_to_string("visitor/visitor_notification_email.html", context)
#     email_plaintext_message = strip_tags(email_html_message)
#     subject = "Visitor Notification"
#     email_from = 'jadenik13@gmail.com'
#     to_email = employee.email
#     try:
#         # Create the email message
#         msg = EmailMultiAlternatives(
#             subject,
#             email_plaintext_message,
#            # from_email,
#             [to_email],
#         )

#         # Attach the HTML content
#         msg.attach_alternative(email_html_message, "text/html")

#         # Attach the image
#         img_dir = 'static'
#         image = 'logo.png'
#         file_path = os.path.join(img_dir, image)
#         with open(file_path, 'rb') as f:
#             img = MIMEImage(f.read())
#             img.add_header('Content-ID', '<{name}>'.format(name=image))
#             img.add_header('Content-Disposition', 'inline', filename=image)
#             msg.attach(img)

#         # Send the email
#         msg.send()

#         return JsonResponse({'success': True, 'message': 'Email sent successfully'})
#     except Exception as e:
#         return JsonResponse({'success': False, 'message': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@require_POST
def checkout_visitor(request):
    """
    Function for visitor checkout
    """
    if request.method == "POST":
        data = json.loads(request.body)
        visit_id = data.get("visit_id")
        checkout_time_str = data.get("checkout_time")

        try:
            visit = Visit.objects.get(id=visit_id)
            checkout_time = timezone.datetime.fromisoformat(
                checkout_time_str
            ).astimezone(pytz.timezone("Asia/Kolkata"))
            visit.check_out = checkout_time
            visit.save()
            return JsonResponse({"success": True})
        except Visit.DoesNotExist:
            return JsonResponse({"success": False, "error": "Visit does not exist"})
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"})


@csrf_exempt
def fetch_visitor_details(request):
    """
    Function to fetch all visitor details by just entering the mobile number
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            mobile_number = data.get("mobile_number", None)
            if mobile_number:
                try:
                    visitor = VisitorProfile.objects.get(mobile_number=mobile_number)
                    visitor_data = {
                        "full_name": visitor.full_name,
                        "email": visitor.email,
                        "mobile_number": visitor.mobile_number,
                        "photo_url": visitor.photo.url if visitor.photo else None,
                    }
                    return JsonResponse(visitor_data)
                except VisitorProfile.DoesNotExist:
                    return JsonResponse(
                        {"error": "Visitor not found"}, status=HTTP_404_NOT_FOUND
                    )
            else:
                return JsonResponse(
                    {"error": "Mobile number is required"}, status=HTTP_400_BAD_REQUEST
                )
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON format"}, status=HTTP_400_BAD_REQUEST
            )
    else:
        return JsonResponse(
            {"error": "Only POST requests are allowed"},
            status=HTTP_405_METHOD_NOT_ALLOWED,
        )


def visitor_data_with_visit_details(request):
    """
    To fetch all the records for generating the report (using prefetch related)
    """
    visitors_with_visit_details = []
    user = request.user
    _, organisation_names, units_in_organisations = organisations_details(user)

    visitors = Visit.objects.select_related("gate").filter(
        gate__unit__in=units_in_organisations
    )

    for visit in visitors:
        visitor_details = {
            "visitor_name": visit.visitor.full_name,
            "visitor_phone": visit.visitor.mobile_number,
            "visitor_address": visit.visitor.address,
            "visitor_email": visit.visitor.email,
            "visitor_purpose": visit.purpose,
            "visitor_employee": visit.employee,
            "visitor_checkIN": visit.check_in,
            "visitor_checkOut": visit.check_out,
            "visitor_gate": visit.gate.name,
            "visitor_unit": visit.gate.unit.name,
            "is_active": visit.is_active,
        }
        visitors_with_visit_details.append(visitor_details)

    # Pagination
    visitors_per_page = 5
    paginator = Paginator(visitors_with_visit_details, visitors_per_page)
    page_number = request.GET.get("page")

    try:
        visitors = paginator.page(page_number)
    except PageNotAnInteger:
        visitors = paginator.page(1)
    except EmptyPage:
        visitors = paginator.page(paginator.num_pages)

    return render(
        request,
        "visitor/report.html",
        {
            "visitors_with_visit_details": visitors,
            "organisation_names": organisation_names,
        },
    )


@csrf_exempt
def fetch_visitor_details_by_date(request):
    """
    To fetch visitor details by specific date
    """
    if request.method == "POST":

        filter_date = None
        try:
            if filter_date in request.GET:
                date = datetime.strptime(request.GET["filter_date"], "%Y-%m-%d")
            else:
                date = datetime.now()

            year = date.strftime("%Y")
            month = date.strftime("%m")
            day = date.strftime("%d")
            filter_date = date

            data = json.loads(request.body.decode("utf-8"))
            check_in_date = data.get("check_in", None)

            if check_in_date:
                visits = Visit.objects.filter(check_in__date=check_in_date)
                if visits.exists():
                    visitors_data = []
                    for visit in visits:
                        visitor_data = {
                            "full_name": visit.visitor.full_name,
                            "email": visit.visitor.email,
                            "mobile_number": visit.visitor.mobile_number,
                            "photo_url": (
                                visit.visitor.photo.url if visit.visitor.photo else None
                            ),
                            "purpose": visit.purpose,
                            "address": visit.visitor.address,
                            "check_in": visit.check_in.strftime("%Y-%m-%d %I:%M %p"),
                            "check_out": (
                                visit.check_out.strftime("%Y-%m-%d %I:%M %p")
                                if visit.check_out
                                else None
                            ),
                            "gate": visit.gate.name,
                            "employee": visit.employee.full_name,
                            "department": visit.employee.department.name,
                            "unit": visit.employee.department.unit.name,
                            "organisation": visit.employee.department.org.name,
                            "filter_date": filter_date,
                        }
                        visitors_data.append(visitor_data)
                    return JsonResponse(visitors_data, safe=False)
                else:
                    return JsonResponse(
                        {"error": "No visitors found for the given date"}, status=404
                    )

            else:
                return JsonResponse({"error": "Date is required"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    else:
        return HttpResponseNotAllowed(["POST"])


@csrf_exempt
def fetch_visitor_details_by_date_range(request):
    """
    Function to fetch all visitor details within a date range
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            start_date = data.get("start_date")
            end_date = data.get("end_date")

            if not start_date or not end_date:
                return JsonResponse(
                    {"error": "Start date and end date are required"},
                    status=HTTP_400_BAD_REQUEST,
                )

            visits = Visit.objects.filter(
                Q(check_in__date__gte=start_date) & Q(check_in__date__lte=end_date)
            )

            if visits.exists():
                visitors_data = []
                for visit in visits:
                    visitor_data = {
                        "full_name": visit.visitor.full_name,
                        "email": visit.visitor.email,
                        "mobile_number": visit.visitor.mobile_number,
                        "photo_url": (
                            visit.visitor.photo.url if visit.visitor.photo else None
                        ),
                        "purpose": visit.purpose,
                        "check_in": visit.check_in,
                        "check_out": visit.check_out,
                        "gate": visit.gate.name,
                        "employee": visit.employee.full_name,
                        "unit": visit.employee.department.unit.name,
                        "organisation": visit.employee.department.org.name,
                    }
                    visitors_data.append(visitor_data)
                return JsonResponse(visitors_data, safe=False)
            else:
                return JsonResponse(
                    {"error": "No visitors found for the given date range"},
                    status=HTTP_404_NOT_FOUND,
                )

        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON format"}, status=HTTP_400_BAD_REQUEST
            )


def most_visited_employee_details():
    """
    For fetching the details of most visited employee by visitor
    """
    employee_visit_counts = Visit.objects.values("employee").annotate(
        visit_count=Count("employee")
    )

    most_visited_employee = employee_visit_counts.order_by("-visit_count").first()

    if most_visited_employee:
        employee_details = EmployeeProfile.objects.get(
            id=most_visited_employee["employee"]
        )

        response_data = {
            "employee_id": employee_details.id,
            "full_name": employee_details.full_name,
            "visit_count": most_visited_employee["visit_count"],
            "department_name": employee_details.department.name,
        }

        return {"employee_data": response_data}
    else:
        return JsonResponse({"error": "No visits recorded yet"})


@csrf_exempt
def total_visitors_by_date(request):
    """
    To display the total numbers of visitor for specific
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            date_str = data.get("date")
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON format in request body"},
                status=HTTP_400_BAD_REQUEST,
            )
    else:
        return JsonResponse(
            {"error": "Only POST requests are allowed"},
            status=HTTP_405_METHOD_NOT_ALLOWED,
        )

    if not date_str:
        return JsonResponse(
            {"error": "Date parameter is required"}, status=HTTP_400_BAD_REQUEST
        )

    try:
        date = make_aware(datetime.strptime(date_str, "%Y-%m-%d"))

    except ValueError:
        return JsonResponse(
            {"error": "Invalid date format. Use YYYY-MM-DD"},
            status=HTTP_400_BAD_REQUEST,
        )

    visits = Visit.objects.filter(check_in__date=date)
    total_visitors = visits.count()

    return JsonResponse({"date": date_str, "total_visitors": total_visitors})


@csrf_exempt
def total_visitors_by_date_range(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            start_date_str = data.get("start_date")
            end_date_str = data.get("end_date")
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON format in request body"},
                status=HTTP_400_BAD_REQUEST,
            )
    else:
        return JsonResponse(
            {"error": "Only POST requests are allowed"},
            status=HTTP_405_METHOD_NOT_ALLOWED,
        )

    if not start_date_str or not end_date_str:
        return JsonResponse(
            {"error": "Both start_date and end_date parameters are required"},
            status=HTTP_400_BAD_REQUEST,
        )

    try:
        start_date = make_aware(datetime.strptime(start_date_str, "%Y-%m-%d"))

        end_date = make_aware(datetime.strptime(end_date_str, "%Y-%m-%d"))

    except ValueError:
        return JsonResponse(
            {"error": "Invalid date format. Use YYYY-MM-DD"},
            status=HTTP_400_BAD_REQUEST,
        )

    visits = Visit.objects.filter(check_in__date__range=[start_date, end_date])
    total_visitors = visits.count()
    return JsonResponse(
        {
            "start_date": start_date_str,
            "end_date": end_date_str,
            "total_visitors": total_visitors,
        }
    )


def view_gatepass(request, visit_id):
    """
    Function to generate visitor pass
    """
    visit = get_object_or_404(Visit, id=visit_id)
    context = {
        "visitor": visit.visitor,
        "visit": visit,
    }
    return render(request, "visitor/gatepass.html", context)


def downaload_visitor_report(request):
    """
    Function for downloading the report in an Excel sheet
    """
    # TODO: need to revisit for refactor the code
    user = request.user
    visitors_with_visit_details = []

    _, organisation_names, units_in_organisations = organisations_details(user)

    visitors = Visit.objects.select_related("gate").filter(
        gate__unit__in=units_in_organisations
    )

    for visit in visitors:
        visitor_details = {
            "visitor_name": visit.visitor.full_name,
            "visitor_phone": visit.visitor.mobile_number,
            "visitor_address": visit.visitor.address,
            "visitor_email": visit.visitor.email,
            "visitor_purpose": visit.purpose,
            "visitor_employee": visit.employee,
            "visitor_department": visit.employee.department,
            "visitor_checkIn": visit.check_in,
            "visitor_checkOut": visit.check_out,
            "visitor_gate": visit.gate.name,
            "visitor_unit": visit.gate.unit.name,
        }
        visitors_with_visit_details.append(visitor_details)

    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output, {"remove_timezone": True})
    worksheet = workbook.add_worksheet()

    bold_format = workbook.add_format(
        {
            "bold": True,
            "bg_color": "#005577",
            "color": "white",
            "align": "center",
        }
    )

    date_format = workbook.add_format({"num_format": "mmmm dd, yyyy hh:mm AM/PM"})

    headers = [
        "Visitor Name",
        "Visitor Email",
        "Visitor Phone",
        "Visitor Address",
        "Check In",
        "Check Out",
        "Employee Name",
        "Visitor Department",
        "Unit",
        "Gate",
    ]
    left_align_format = workbook.add_format({"align": "left"})
    heading = workbook.add_format(
        {
            "align": "center",
            "font_size": 24,
            "bg_color": "#005577",
            "bold": True,
            "color": "white",
        }
    )
    heading1 = workbook.add_format(
        {
            "align": "center",
            "font_size": 14,
            "bg_color": "#005577",
            "bold": True,
            "color": "white",
        }
    )

    worksheet.merge_range("E1:H1", "Visitor Report", heading)
    for name in organisation_names:
        worksheet.merge_range("E2:H2", f"{name}", heading1)

    # Increase the height of row 2
    worksheet.set_row(0, 30)  # Index starts at 0, so row 2 is index 1

    for col, header in enumerate(headers):
        worksheet.write(3, col, header, bold_format)

    row = 4
    for visitor_details in visitors_with_visit_details:
        worksheet.write(row, 0, visitor_details["visitor_name"], left_align_format)
        worksheet.write(row, 1, visitor_details["visitor_email"], left_align_format)
        worksheet.write(row, 2, visitor_details["visitor_phone"], left_align_format)
        worksheet.write(row, 3, visitor_details["visitor_address"], left_align_format)
        worksheet.write(row, 4, visitor_details["visitor_checkIn"], date_format)
        worksheet.write(row, 5, visitor_details["visitor_checkOut"] or "N/A", date_format)
        worksheet.write(row, 6, visitor_details["visitor_employee"].full_name, left_align_format)
        worksheet.write(row, 7, visitor_details["visitor_department"].name, left_align_format)
        worksheet.write(row, 8, visitor_details["visitor_unit"], left_align_format)
        worksheet.write(row, 9, visitor_details["visitor_gate"], left_align_format)
        row += 1

    worksheet.set_column("A:A", 15)
    worksheet.set_column("B:B", 25)
    worksheet.set_column("C:C", 15)
    worksheet.set_column("D:D", 30)
    worksheet.set_column("E:F", 25)
    worksheet.set_column("G:G", 25)
    worksheet.set_column("H:H", 25)
    worksheet.set_column("I:I", 20)
    worksheet.set_column("J:J", 25)

    workbook.close()

    current_datetime_utc = datetime.utcnow()

    ist_timezone = pytz.timezone("Asia/Kolkata")
    current_datetime_ist = current_datetime_utc.astimezone(ist_timezone)
    filename = current_datetime_ist.strftime("visitor_report_%Y-%m-%d_%I:%M:%S %p.xlsx")

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename={filename}"
    output.seek(0)
    response.write(output.read())

    return response


def visitor_analytics(request):
    """
    Function for getting visitor count as per department
    """
    user = request.user
    organisations, _, units_in_organisations = organisations_details(user)
    if request.method == "GET":
        today = datetime.now().date()
        month_start = datetime(today.year, today.month, 1)
        week_start = today - timedelta(days=today.weekday())
        weekly_visitors_data = []

        visits = Visit.objects.select_related("gate").filter(gate__unit__in=units_in_organisations)

        for i in range(4):
            week_end = week_start + timedelta(days=6)
            weekly_visitors_count = (
                visits.filter(check_in__date__range=[week_start, week_end]).count()
            )
            weekly_visitors_data.append(
                {"week": f"Week {i + 1}", "visitors_count": weekly_visitors_count}
            )
            week_start = week_end + timedelta(days=1)

        # Fetch visitor counts for each month
        monthly_visitor_data = []
        for i in range(1, 13):
            month_start = datetime(datetime.now().year, i, 1)
            month_end = month_start.replace(
                day=calendar.monthrange(month_start.year, month_start.month)[1]
            )
            monthly_visitors_count = (
                visits.filter(check_in__date__range=[month_start, month_end])
                .count()
            )
            monthly_visitor_data.append(monthly_visitors_count)

        monthly_visitor_counts_json = json.dumps(monthly_visitor_data)
        departments_with_count = (
            Department.objects.select_related("org")
            .prefetch_related("dept_emp__permissions__user_acc")
            .filter(org__in=organisations)
            .annotate(
                visitor_count=Count("dept_emp__visit_employee__visitor", distinct=True)
            )
        )

        departments_visitor_data = {"categories": [], "data": []}

        for department in departments_with_count:
            department_name = department.name
            visitor_count = department.visitor_count
            departments_visitor_data["categories"].append(department_name)
            departments_visitor_data["data"].append(visitor_count)

        # Convert QuerySet to list of dictionaries
        departments_with_count_list = list(
            departments_with_count.values("name", "visitor_count")
        )
        active_departments = Department.objects.filter(is_active=True)

        # Calculate yesterday's date
        yesterday = datetime.now() - timedelta(days=1)

        # Fetch yesterday's visitors count
        yesterdays_visitors_count = (
            Visit.objects.select_related("gate")
            .filter(gate__unit__in=units_in_organisations)
            .filter(check_in__date=yesterday.date())
            .count()
        )

        # Fetch visitor counts for the past week

        week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        weekly_visitors_count = (
            visits.filter(check_in__date__range=[week_start, week_end])
            .count()
        )

        # Fetch visitor counts for the past month
        month_start = datetime(datetime.now().year, datetime.now().month, 1)

        monthly_visitors_count = (
            visits.filter(check_in__date__gte=month_start.date()).count()
        )
        # Fetch visitor counts for the past year
        year_start = datetime(datetime.now().year, 1, 1)
        yearly_visitors_count = (
            visits.filter(check_in__date__gte=year_start.date()).count()
        )

        overall_visitors_count = (
            visits.count()

        )

        # Fetch the most visited purpose and its visit count
        most_visited_purpose = (
            Visit.objects.values("purpose")
            .annotate(visit_count=Count("purpose"))
            .order_by("-visit_count")
            .first()
        )

        most_visited_purpose_details = None
        if most_visited_purpose:
            most_visited_purpose_details = {
                "purpose": most_visited_purpose["purpose"],
                "visit_count": most_visited_purpose["visit_count"],
            }

        # Fetch the most visited employee and their visiting count
        employee_visit_counts = Visit.objects.values("employee").annotate(
            visit_count=Count("employee")
        )
        most_visited_employee = employee_visit_counts.order_by("-visit_count").first()

        most_visited_employee_details = None
        if most_visited_employee:
            employee_details = EmployeeProfile.objects.get(
                id=most_visited_employee["employee"]
            )
            department_name = employee_details.department.name

            most_visited_employee_details = {
                "employee_name": employee_details.full_name,
                "visit_count": most_visited_employee["visit_count"],
                "department_name": department_name,
            }

        today = timezone.now().date()
        todays_visitors_count = Visit.objects.filter(gate__unit__in=units_in_organisations).filter(
            check_in__date=today).count()

        return render(
            request,
            "organisation/analytics.html",
            {
                "departments_visitor_data": departments_visitor_data,
                "active_departments": list(active_departments.values()),
                "most_visited_employee_details": most_visited_employee_details,
                "todays_visitors_count": todays_visitors_count,
                "active_departments_count": active_departments.count(),
                "departments_with_count": departments_with_count_list,
                "yesterdays_visitors_count": yesterdays_visitors_count,
                "weekly_visitors_count": weekly_visitors_count,
                "monthly_visitors_count": monthly_visitors_count,
                "yearly_visitors_count": yearly_visitors_count,
                "overall_visitors_count": overall_visitors_count,
                "most_visited_purpose_details": most_visited_purpose_details,
                "monthly_visitor_counts_json": monthly_visitor_counts_json,
            },
        )




def weekly_visitor_count(request):
    
    """
        Function for Graphs
    """
    if request.method == "GET":
        today = datetime.now().date()
        weekly_visitors_data = []
        user = request.user
        for i in range(3, -1, -1):
            week_start = today - timedelta(days=today.weekday() + 7 * i)
            week_end = week_start + timedelta(days=6)

            _, _, units_in_organisations = organisations_details(user)

            weekly_visitors_count = (
                Visit.objects.select_related("gate")
                .filter(gate__unit__in=units_in_organisations)
                .filter(check_in__date__range=[week_start, week_end])
                .count()
            )

            weekly_visitors_data.append(
                {"week": f"Week {4 - i}", "visitors_count": weekly_visitors_count}
            )

        return JsonResponse({"weekly_visitors_data": weekly_visitors_data})


def visit_purpose_graph(request):
    organisations = Organisation.objects.filter(
        dept_org__dept_emp__permissions__user_acc=request.user
    )
    units_in_organisations = Unit.objects.filter(org__in=organisations)
    visit_purpose_counts = (
        Visit.objects.select_related("gate")
        .filter(gate__unit__in=units_in_organisations)
        .values("purpose")
        .annotate(count=Count("purpose"))
        .order_by("-count")[:5]
    )
    purposes = [item["purpose"] for item in visit_purpose_counts]
    counts = [item["count"] for item in visit_purpose_counts]
    return JsonResponse({"purposes": purposes, "counts": counts})


def update_visitor(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    visitor = visit.visitor
    if request.method == "POST":
        form = UpdateVisitorForm(request.POST, instance=visitor)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UpdateVisitorForm(instance=visitor)

    return render(
        request, "visitor/update_visitor.html", {"form": form, "visit": visit}
    )


def split_full_name(full_name):
    # Utility function to split full name into first, middle, and last name
    parts = full_name.split()
    first_name = parts[0]
    middle_name = ' '.join(parts[1:-1]) if len(parts) > 2 else ''
    last_name = parts[-1] if len(parts) > 1 else ''
    return first_name, middle_name, last_name


def visitor_registration(request, gate_id):
    gate = get_object_or_404(Gate, id=gate_id)
    gate_name = gate.name
    unit_name = gate.unit.name
    unit_id = gate.unit.id
    organisations_details = gate.unit.org.name
    org_id = gate.unit.org.id

    # Generate the URL
    base_url = request.build_absolute_uri("/")
    visitor_url = (
        f"{base_url}visitor/gate/{gate_id}/visitor_form/"
    )

    # Generate QR Code
    qr_code_filename = f"qr_code_{gate_id}.png"
    qr_code_path = generate_qr_code(visitor_url, qr_code_filename)

    employees = EmployeeProfile.objects.filter(department__unit__id=unit_id)
    employee_names = [(str(emp.id), f"{emp.first_name} {emp.last_name}") for emp in employees]

    if request.method == "POST":
        visitor_fm = VisitorProfileForm(request.POST, request.FILES)
        visit_fm = VisitForm(None, request.POST)
        check_in_time_utc = timezone.now()

        if visitor_fm.is_valid() and visit_fm.is_valid():
            created_by = request.user if request.user.is_authenticated else None

            # Retrieve cleaned data from visitor form
            visitor_data = visitor_fm.cleaned_data
            full_name = visitor_data.get("full_name")
            first_name, middle_name, last_name = split_full_name(full_name)

            # Create VisitorProfile instance without saving it to the database yet
            visitor_profile = visitor_fm.save(commit=False)
            visitor_profile.first_name = first_name
            visitor_profile.middle_name = middle_name
            visitor_profile.last_name = last_name
            visitor_profile.created_by = created_by
            visitor_profile.updated_by = created_by
            visitor_profile.save()

            # Create Visit instance linked to the created VisitorProfile
            visit = visit_fm.save(commit=False)
            visit.visitor = visitor_profile
            visit.check_in = check_in_time_utc
            visit.created_by = created_by
            visit.updated_by = created_by
            visit.save()

            messages.success(request, "Visitor registered successfully!")

            return render(
                request, "selfreg_gp.html", {"visitor": visitor_profile, "visit": visit}
            )

        else:
            # Debugging: Print form errors
            logging.debug("VisitorProfileForm errors: %s", visitor_fm.errors)
            logging.debug("VisitForm errors: %s", visit_fm.errors)

    else:
        visitor_fm = VisitorProfileForm()
        visit_fm = VisitForm(user=request.user, initial={"gate": gate})

    return render(
        request,
        "self_registration.html",
        {
            "organisations_details": organisations_details,
            "visitor_fm": visitor_fm,
            "visit_fm": visit_fm,
            "employee_names": employee_names,
            "gate_id": gate_id,
        },
    )

def visitor_self_registration(request, gate_id):
    gate = get_object_or_404(Gate, id=gate_id)
    gate_name = gate.name
    unit_name = gate.unit.name
    unit_id = gate.unit.id
    organisations_details = gate.unit.org.name
    org_id = gate.unit.org.id
    unit = gate.unit
    employees = EmployeeProfile.objects.filter(department__unit__id=unit.id)
    employee_names = [(str(emp.id), f"{emp.first_name} {emp.last_name}") for emp in employees]

    visitor_profile = None
    last_met_employee = None
    mobile_number = None

    if request.method == 'POST':
        if 'mobile_number' in request.POST:
            mobile_number = request.POST.get('mobile_number')
            if VisitorProfile.objects.filter(mobile_number=mobile_number).exists():
                visitor_profile = VisitorProfile.objects.filter(mobile_number=mobile_number).first()
                last_visit = Visit.objects.filter(visitor=visitor_profile).order_by('-check_in').first()
                if last_visit:
                    last_met_employee = last_visit.employee
                    last_purpose = last_visit.purpose or "Default Purpose"
                    messages.info(request, f"Do you want to meet {last_met_employee} you met last time?")
                else:
                    messages.info(request, "This is your first visit.")
            else:
                return redirect(reverse('visitor_registration', args=[gate_id]))

        else:
            visitor_profile_id = request.POST.get('visitor_profile_id')
            visitor_profile = get_object_or_404(VisitorProfile, id=visitor_profile_id)
            # Convert UTC time to IST
            check_in_time_utc = timezone.now()

            employee = request.POST.get('employee')
            purpose = request.POST.get('purpose')

            last_visit = Visit.objects.filter(visitor=visitor_profile).order_by('-check_in').first()
            no_of_individuals = request.POST.get('no_of_individuals', 1)

            visit = Visit.objects.create(
                visitor=visitor_profile,
                employee_id=employee or last_visit.employee.id,
                check_in=check_in_time_utc,
                gate=gate,
                purpose=purpose or last_visit.purpose,
                no_of_individuals=no_of_individuals
            )

            return render(request, "selfreg_gp.html",  {
                "visitor": visit.visitor,
                "visit": visit,
            })

    return render(request, "visitor/add_self_visit_details.html", {
        'gate_name': gate_name,
        'unit_name': unit_name,
        'unit_id': unit_id,
        'organisations_details': organisations_details,
        'org_id': org_id,
        'visitor_profile': visitor_profile,
        'mobile_number': mobile_number,
        'last_met_employee': last_met_employee,
        'employee_names': employee_names,
    })




def generate_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img_path = os.path.join(settings.MEDIA_ROOT, filename)
    img.save(img_path)
    return os.path.join(settings.MEDIA_URL, filename)


def get_visitor_profile(request):
    user = request.user
    organisations, organisation_names, _ = organisations_details(user)
    employees = EmployeeProfile.objects.select_related("department").filter(
        department__org__in=organisations
    )

    employee_names = [(str(emp.id), f"{emp.first_name} {emp.last_name}") for emp in employees]
    units = Unit.objects.filter(org__in=organisations)
    gates = Gate.objects.filter(unit__in=units)

    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            mobile_number = data.get('mobile_number')

            if mobile_number:
                logging.info(f"Mobile Number: {mobile_number}")
            else:
                logging.warning("Mobile number is required.")
                return HttpResponseBadRequest(json.dumps({'error': 'Mobile number is required.'}),
                                              content_type="application/json")

            try:
                visitor_profile = VisitorProfile.objects.get(mobile_number=mobile_number)
                response_data = {
                    'exists': True,
                    'email': visitor_profile.email,
                    'mobile_number': visitor_profile.mobile_number,
                    'photo': request.build_absolute_uri(visitor_profile.photo.url) if visitor_profile.photo else None,
                    'first_name': visitor_profile.first_name,
                    'middle_name': visitor_profile.middle_name,
                    'last_name': visitor_profile.last_name,
                    'full_name': visitor_profile.full_name,
                    'address': visitor_profile.address,
                }

                if 'check_in' in data:
                    visit_form = VisitForm(request.user, data)
                    if visit_form.is_valid():
                        visit_instance = visit_form.save(commit=False)
                        visit_instance.visitor = visitor_profile
                        visit_instance.save()
                        return JsonResponse({'success': True, 'message': 'Visit details submitted successfully'})
                    else:
                        return JsonResponse({'success': False, 'errors': visit_form.errors}, status=400)

            except VisitorProfile.DoesNotExist:
                response_data = {'exists': False}

            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return HttpResponseBadRequest(json.dumps({'error': 'Invalid JSON.'}), content_type="application/json")
    elif request.method == 'GET':
        visit_form = VisitForm(request.user)
        return render(request, 'visitor/add_visit_details.html',
                      {'visit_form': visit_form, 'employees': employee_names, 'gates': gates})
    else:
        return HttpResponseNotAllowed(['POST', 'GET'], json.dumps({'error': 'Invalid request method.'}),
                                      content_type="application/json")



def submit_visit_details(request):
    """
    Create Visit Details
    """
    if request.method == 'POST':
        try:
            mobile_number = request.POST.get('mobile_number', '')
            purpose = request.POST.get('purpose', '')
            check_in = request.POST.get('check_in', '')
            no_of_individuals = request.POST.get('no_of_individuals', '')
            vehicle_number = request.POST.get('vehicle_number', '')
            employee_id = request.POST.get('employee', '')
            gate = request.POST.get('gate', '')

            gate = Gate.objects.get(id=gate)
            visitor = VisitorProfile.objects.get(mobile_number=mobile_number)
            employee = EmployeeProfile.objects.get(id=employee_id)

            visit = Visit.objects.create(
                purpose=purpose,
                check_in=check_in,
                no_of_individuals=no_of_individuals,
                vehicle_number=vehicle_number,
                visitor=visitor,
                employee=employee,
                gate=gate,
            )

            # Send email notification
            # send_django_email(visitor, employee, visit)
            return render(request, 'visitor/thank_you.html')
        except ObjectDoesNotExist as e:
            return JsonResponse({'success': False, 'message': str(e)}, HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({'error': 'Method not allowed'}, HTTP_405_METHOD_NOT_ALLOWED)


def submit_self_visit_details(request):
    """
    Create Visit Details
    """
    if request.method == 'POST':
        try:
            mobile_number = request.POST.get('mobile_number', '')
            purpose = request.POST.get('purpose', '')
            check_in = request.POST.get('check_in', '')
            no_of_individuals = request.POST.get('no_of_individuals', '')
            vehicle_number = request.POST.get('vehicle_number', '')
            employee_id = request.POST.get('employee', '')
            gate_id = request.POST.get('gate', '')

            # Ensure gate and employee fields are correctly fetched
            gate = get_object_or_404(Gate, id=gate_id)
            visitor = get_object_or_404(VisitorProfile, mobile_number=mobile_number)
            employee = get_object_or_404(EmployeeProfile, id=employee_id)

            visit = Visit.objects.create(
                purpose=purpose,
                check_in=check_in,
                no_of_individuals=no_of_individuals,
                vehicle_number=vehicle_number,
                visitor=visitor,
                employee=employee,
                gate=gate,
            )

            # Send email notification
            # send_django_email(visitor, employee, visit)

            # Generate the URL
            base_url = request.build_absolute_uri("/")
            visitor_url = f"{base_url}visitor/gate/{gate_id}/visitor_form/"

            # Generate QR Code
            qr_code_filename = f"qr_code_{gate_id}.png"
            qr_code_path = generate_qr_code(visitor_url, qr_code_filename)

            # Fetch employees for the specified unit
            employees = EmployeeProfile.objects.filter(department__unit__id=gate.unit.id)
            employee_names = [(str(emp.id), f"{emp.first_name} {emp.last_name}") for emp in employees]

            return render(
                request,
                'selfreg_gp.html',
                {
                    'visitor': visitor,
                    'visit': visit,
                    'qr_code_path': qr_code_path,
                    'employee_names': employee_names,
                    'gate_name': gate.name,
                    'unit_name': gate.unit.name,
                    'organisations_details': gate.unit.org.name,
                }
            )
        except ObjectDoesNotExist as e:
            return JsonResponse({'success': False, 'message': str(e)}, HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({'error': 'Method not allowed'}, HTTP_405_METHOD_NOT_ALLOWED)







