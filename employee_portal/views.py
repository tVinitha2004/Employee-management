from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Employee
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Attendance
from django.http import JsonResponse
from datetime import date, timedelta
from calendar import monthrange
from django.db.models import Sum
from django.contrib import messages
from django.contrib import admin
from .models import Holiday


@login_required
def my_account(request):
    user = request.user
    emp = Employee.objects.filter(user=user).first()
    return render(request, "my_account.html", {"user": user, "emp": emp})


def employee_list(request):

    if request.method == "POST":
        # Get data from form
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        official_email = request.POST.get("official_email")
        phone = request.POST.get("phone")
        uan_number = request.POST.get("uan_number")
        aadhaar_number = request.POST.get("aadhaar_number")
        pan_number = request.POST.get("pan_number")
        photo = request.FILES.get("photo")
        # address
        present_address_line1 = request.POST.get("present_address_line1")
        present_address_line2 = request.POST.get("present_address_line2")
        present_city = request.POST.get("present_city")
        present_state = request.POST.get("present_state")
        present_country = request.POST.get("present_country")
        present_postal_code = request.POST.get("present_postal_code")
        # permanent
        permanent_same_as_present = request.POST.get("permanent_same_as_present")
        permanent_address_line1 = request.POST.get("permanent_address_line1")
        permanent_address_line2 = request.POST.get("permanent_address_line2")
        permanent_city = request.POST.get("permanent_city")
        permanent_state = request.POST.get("permanent_state")
        permanent_country = request.POST.get("permanent_country")
        permanent_postal_code = request.POST.get("permanent_postal_code")
        # professional
        experience = request.POST.get("experience")
        source_of_hire = request.POST.get("source_of_hire")
        skill_set = request.POST.get("skill_set")
        highest_qualification = request.POST.get("highest_qualification")
        additional_information = request.POST.get("additional_information")
        location = request.POST.get("location")
        title = request.POST.get("title")
        current_salary = request.POST.get("current_salary")

        if current_salary == "" or current_salary is None:
            current_salary = None
        else:
            try:
                current_salary = float(current_salary)
            except ValueError:
                current_salary = None
        department = request.POST.get("department")
        offer_letter = request.POST.get("offer_letter")

        # education
        college_name = request.POST.get("college_name")
        degree = request.POST.get("degree")
        field_of_study = request.POST.get("field_of_study")
        year_of_completion = request.POST.get("year_of_completion")

        # work
        occupation = request.POST.get("occupation")
        company = request.POST.get("company")
        summary = request.POST.get("summary")
        duration = request.POST.get("duration")
        currently_work_here = request.POST.get("currently_work_here")

        tentative_joining_date = request.POST.get("tentative_joining_date")
        if tentative_joining_date == "" or tentative_joining_date is None:
            tentative_joining_date = None
        else:
            try:
                tentative_joining_date = datetime.strptime(
                    tentative_joining_date, "%Y-%m-%d"
                ).date()
            except ValueError:
                tentative_joining_date = None

        year_of_completion = request.POST.get("year_of_completion")
        if year_of_completion == "" or year_of_completion is None:
            year_of_completion = None
        else:
            try:
                year_of_completion = datetime.strptime(
                    year_of_completion, "%Y-%m-%d"
                ).date()
            except ValueError:
                year_of_completion = None

        # Create Employee
        Employee.objects.create(
            first_name=first_name,
            last_name=last_name,
            official_email=official_email,
            phone=phone,
            uan_number=uan_number,
            aadhaar_number=aadhaar_number,
            pan_number=pan_number,
            photo=photo,
            present_address_line1=present_address_line1,
            present_address_line2=present_address_line2,
            present_city=present_city,
            present_state=present_state,
            present_country=present_country,
            present_postal_code=present_postal_code,
            permanent_same_as_present=permanent_same_as_present,
            permanent_address_line1=permanent_address_line1,
            permanent_address_line2=permanent_address_line2,
            permanent_city=permanent_city,
            permanent_state=permanent_state,
            permanent_country=permanent_country,
            permanent_postal_code=permanent_postal_code,
            experience=experience,
            source_of_hire=source_of_hire,
            skill_set=skill_set,
            highest_qualification=highest_qualification,
            additional_information=additional_information,
            location=location,
            title=title,
            current_salary=current_salary,
            department=department,
            offer_letter=offer_letter,
            tentative_joining_date=tentative_joining_date,
            college_name=college_name,
            degree=degree,
            field_of_study=field_of_study,
            year_of_completion=year_of_completion,
            occupation=occupation,
            company=company,
            summary=summary,
            duration=duration,
            currently_work_here=currently_work_here,
        )

        return redirect("employee_list")

    # GET request
    employees = Employee.objects.all()
    paginator = Paginator(employees, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request, "employee_portal/employee_list.html", {"employees": employees}
    )


# edit employee
def edit_employee(request, emp_id):
    emp = get_object_or_404(Employee, id=emp_id)

    # Allow only superuser or same employee to edit
    if not request.user.is_superuser and emp.user != request.user:
        messages.error(request, "You are not allowed to edit this profile.")
        return redirect("my_account")

    if request.method == "POST":
        # Candidate details
        emp.first_name = request.POST.get("first_name")
        emp.last_name = request.POST.get("last_name")
        emp.official_email = request.POST.get("official_email")
        emp.phone = request.POST.get("phone")
        emp.uan_number = request.POST.get("uan_number")
        emp.aadhaar_number = request.POST.get("aadhaar_number")
        emp.pan_number = request.POST.get("pan_number")

        # If a new photo is uploaded, update
        if request.FILES.get("photo"):
            emp.photo = request.FILES.get("photo")

        # Address details
        emp.present_address_line1 = request.POST.get("present_address_line1")
        emp.present_address_line2 = request.POST.get("present_address_line2")
        emp.present_city = request.POST.get("present_city")
        emp.present_state = request.POST.get("present_state")
        emp.present_country = request.POST.get("present_country")
        emp.present_postal_code = request.POST.get("present_postal_code")

        emp.permanent_same_as_present = (
            True if request.POST.get("permanent_same_as_present") == "on" else False
        )

        emp.permanent_address_line1 = request.POST.get("permanent_address_line1")
        emp.permanent_address_line2 = request.POST.get("permanent_address_line2")
        emp.permanent_city = request.POST.get("permanent_city")
        emp.permanent_state = request.POST.get("permanent_state")
        emp.permanent_country = request.POST.get("permanent_country")
        emp.permanent_postal_code = request.POST.get("permanent_postal_code")

        # Professional details
        emp.experience = request.POST.get("experience")
        emp.source_of_hire = request.POST.get("source_of_hire")
        emp.skill_set = request.POST.get("skill_set")
        emp.highest_qualification = request.POST.get("highest_qualification")
        emp.additional_information = request.POST.get("additional_information")
        emp.location = request.POST.get("location")
        emp.title = request.POST.get("title")

        salary = request.POST.get("current_salary")
        if salary:
            try:
                emp.current_salary = float(salary)
            except ValueError:
                emp.current_salary = None
        else:
            emp.current_salary = None

        emp.department = request.POST.get("department")

        # If a new offer letter is uploaded
        if request.FILES.get("offer_letter"):
            emp.offer_letter = request.FILES.get("offer_letter")

        # emp.tentative_joining_date = request.POST.get('tentative_joining_date')
        join_date = request.POST.get("tentative_joining_date")
        if join_date:
            try:
                emp.tentative_joining_date = datetime.strptime(
                    join_date, "%Y-%m-%d"
                ).date()
            except ValueError:
                emp.tentative_joining_date = None
        else:
            emp.tentative_joining_date = None

        # Education details
        emp.college_name = request.POST.get("college_name")
        emp.degree = request.POST.get("degree")
        emp.field_of_study = request.POST.get("field_of_study")
        emp.year_of_completion = request.POST.get("year_of_completion")

        # Work Experience details
        emp.occupation = request.POST.get("occupation")
        emp.company = request.POST.get("company")
        emp.summary = request.POST.get("summary")
        emp.duration = request.POST.get("duration")
        emp.currently_work_here = request.POST.get("currently_work_here")

        emp.save()
        messages.success(request, "Your profile has been updated successfully!")

        return redirect(request.META.get("HTTP_REFERER", "dashboard"))


def delete_employee(request, emp_id):

    employee = get_object_or_404(Employee, id=emp_id)

    if request.method == "POST":
        employee.delete()
        return redirect("employee_list")

    return render(
        request, "employee_portal/confirm_delete.html", {"employee": employee}
    )


from datetime import timedelta


@login_required
def dashboard(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        employee = None

    today = timezone.localdate()
    attendance, created = None, None
    if employee:
        try:
            attendance, created = Attendance.objects.get_or_create(
                user=request.user, date=today
            )
        except Attendance.MultipleObjectsReturned:
            # pick first one & delete others
            duplicates = Attendance.objects.filter(user=request.user, date=today)
            attendance = duplicates.first()
            duplicates.exclude(id=attendance.id).delete()

    start_of_week = today - timedelta(
        days=today.weekday() + 1 if today.weekday() < 6 else 0
    )  # Sunday
    end_of_week = start_of_week + timedelta(days=6)  # Saturday

    weekly_summary = []
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        att = Attendance.objects.filter(user=request.user, date=day).first()
        weekday = day.weekday()
        if weekday == 5 or weekday == 6:
            worked = "Weekend"
        elif att and att.duration_seconds:
            hrs = att.duration_seconds // 3600
            mins = (att.duration_seconds % 3600) // 60
            worked = f"{hrs}h {mins}m"
        else:
            worked = "-"
        if att and att.duration_seconds:
            hrs = att.duration_seconds // 3600
            mins = (att.duration_seconds % 3600) // 60
            worked = f"{hrs}h {mins}m"
        else:
            worked = "-"
        weekly_summary.append({"date": day, "worked": worked})

    context = {
        "employee": employee,
        "attendance": attendance,
        "weekly_summary": weekly_summary,
        "today": today,
        "start_of_week": start_of_week,
        "end_of_week": end_of_week,
    }
    return render(request, "employee_portal/dashboard.html", context)


@login_required
def check_browser_close(request):
    """Handle browser close event and mark checkout."""
    today = date.today()
    attendance = Attendance.objects.filter(user=request.user, date=today).first()

    if attendance and attendance.check_in and not attendance.check_out:
        now = datetime.now()
        attendance.check_out = now
        attendance.save()

    return JsonResponse({"message": "Browser closed, timer stopped"})


def myspace_overview(request):
    # Get employee details for current logged-in user
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        employee = None

    return render(request, "employee_portal/dashboard.html", {"emp": employee})


# @login_required
# def toggle_check(request):
#     today = date.today()
#     attendance, created = Attendance.objects.get_or_create(
#         user=request.user, date=today
#     )

#     now = datetime.now()

#     if request.method == "POST":
#         action = request.POST.get("action")
#         duration_from_frontend = request.POST.get("duration")

#         if duration_from_frontend:
#             try:
#                 duration_from_frontend = int(duration_from_frontend)
#             except ValueError:
#                 duration_from_frontend = attendance.duration_seconds
#         else:
#             duration_from_frontend = attendance.duration_seconds

#         # disable checkin after 8 hours
#         if attendance.eight_hours_completed and action == "checkin":
#             return JsonResponse(
#                 {
#                     "status": "eight_hours_completed",
#                     "message": "You’ve already completed 8 working hours for today",
#                 }
#             )

#         if action == "checkin":
#             if not attendance.check_in:
#                 attendance.check_in = now.time()
#                 attendance.check_out = None

#                 attendance.save()
#             return JsonResponse(
#                 {
#                     "status": "checked_in",
#                     "duration_seconds": attendance.duration_seconds,
#                 }
#             )

#         elif action == "checkout":
#             if attendance.check_in:
#                 attendance.duration_seconds = duration_from_frontend
#                 if attendance.duration_seconds >= 28800:
#                     attendance.eight_hours_completed = True
#                 attendance.check_out = now
#                 attendance.save()
#             return JsonResponse(
#                 {
#                     "status": "checked_out",
#                     "duration_seconds": attendance.duration_seconds,
#                 }
#             )

#         elif action == "pause":
#             attendance.duration_seconds = duration_from_frontend
#             if attendance.duration_seconds >= 28800:
#                 attendance.eight_hours_completed = True
#             attendance.save()
#         return JsonResponse(
#             {"status": "paused", "duration_seconds": attendance.duration_seconds}
#         )

#     elif request.method == "GET":
#         data = {
#             "check_in": (
#                 attendance.check_in.strftime("%H:%M:%S")
#                 if attendance.check_in
#                 else None
#             ),
#             "check_out": (
#                 attendance.check_out.strftime("%H:%M:%S")
#                 if attendance.check_out
#                 else None
#             ),
#             "duration_seconds": attendance.duration_seconds,
#             "eight_hours_completed": attendance.eight_hours_completed,
#         }
#         return JsonResponse(data)


# from django.utils import timezone
# from django.http import JsonResponse


def toggle_check(request):
    user = request.user
    today = timezone.localdate()

    attendance, created = Attendance.objects.get_or_create(
        user=user,
        date=today,
        defaults={
            "check_in": None,
            "check_out": None,
            "duration_seconds": 0,
            "start_time": None,
            "is_running": False,
        },
    )

    # --------------- GET ----------------
    if request.method == "GET":
        total = attendance.duration_seconds or 0

        # If session is running, use start_time (datetime) to compute elapsed
        if attendance.start_time and not attendance.check_out:
            elapsed = (timezone.now() - attendance.start_time).total_seconds()
            total += int(elapsed)

        # clamp to 8 hours
        if total >= 28800:
            total = 28800

        return JsonResponse(
            {
                "duration_seconds": total,
                # for backward compat with your frontend:
                "check_in": (
                    attendance.start_time.strftime("%H:%M:%S")
                    if attendance.start_time
                    else None
                ),
                "check_out": (
                    attendance.check_out.strftime("%H:%M:%S")
                    if attendance.check_out
                    else None
                ),
                "is_running": bool(attendance.start_time and not attendance.check_out),
                "eight_hours_completed": total >= 28800,
            }
        )

    # --------------- POST ----------------

    if request.method == "POST":
        action = request.POST.get("action")

        # CHECK-IN
        if action in ("checkin", "check_in"):
            attendance.start_time = timezone.now()
            attendance.check_out = None
            attendance.is_running = True
            attendance.check_in = attendance.start_time.time()
            attendance.save()
            return JsonResponse(
                {
                    "status": "checked_in",
                    "duration_seconds": attendance.duration_seconds,
                }
            )

        # CHECK-OUT (NO EXTRA SECONDS)
        if action in ("checkout", "check_out"):
            now = timezone.now()

            if attendance.start_time:
                elapsed = (now - attendance.start_time).total_seconds()
                attendance.duration_seconds += int(elapsed)  # <— FIXED (accurate)

            # clamp 8 hours
            if attendance.duration_seconds >= 28800:
                attendance.duration_seconds = 28800
                attendance.eight_hours_completed = True
            else:
                attendance.eight_hours_completed = False

            attendance.check_out = now.time()
            attendance.start_time = None
            attendance.is_running = False
            attendance.save()

            status = (
                "eight_hours_completed"
                if attendance.eight_hours_completed
                else "checked_out"
            )
        return JsonResponse(
            {"status": status, "duration_seconds": attendance.duration_seconds}
        )

    # PAUSE — optional save from frontend
    if action == "pause":
        try:
            duration_from_js = int(request.POST.get("duration", 0))
        except:
            duration_from_js = attendance.duration_seconds

        attendance.duration_seconds = duration_from_js
        attendance.save()
        return JsonResponse(
            {"status": "paused", "duration_seconds": attendance.duration_seconds}
        )

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def work_schedule_view(request):
    start_date = date(2025, 10, 12)
    end_date = date(2025, 10, 18)
    today = date.today()

    attendances = Attendance.objects.filter(
        user=request.user, date__range=[start_date, end_date]
    ).order_by("date")

    context = {
        "attendances": attendances,
        "start_date": start_date.strftime("%d-%b-%Y"),
        "end_date": end_date.strftime("%d-%b-%Y"),
        "general_shift_start": "09:30 AM",
        "general_shift_end": "06:30 PM",
        "today": today,
    }
    return render(request, "dashboard.html", context)


# --------------calender ---------------------------------------------------------------------------------------------


@login_required
def attendance_calendar(request):
    year = int(request.GET.get("year", timezone.localdate().year))
    month = int(request.GET.get("month", timezone.localdate().month))

    start_date = date(year, month, 1)

    # Handle December → January transition
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)

    end_date = next_month - timedelta(days=1)

    days = []
    current_day = start_date

    # holiday
    from .models import Holiday

    holidays = {h.date: h.description for h in Holiday.objects.filter(date__year=year)}

    # Calculate total seconds for the month
    total_seconds = (
        Attendance.objects.filter(user=request.user, date__year=year, date__month=month)
        .exclude(date__in=holidays.keys())
        .aggregate(Sum("duration_seconds"))["duration_seconds__sum"]
        or 0
    )

    total_hours = total_seconds // 3600
    total_minutes = (total_seconds % 3600) // 60

    while current_day <= end_date:
        attendance = Attendance.objects.filter(
            user=request.user, date=current_day
        ).first()

        holiday_description = None

        # Default
        status = "Absent"
        color = "red"
        hours = None

        if current_day in holidays:
            status = "Holiday"
            color = "yellow"
            hours = None
            holiday_description = holidays[current_day]

        if attendance and attendance.duration_seconds > 0:
            h = attendance.duration_seconds // 3600
            m = (attendance.duration_seconds % 3600) // 60
            hours = f"{h:02d}:{m:02d}"
            status = "Present"
            color = "green"

        else:
            hours = None
            status = "Absent"
            color = "red"

            # holiday
        is_holiday = current_day in holidays

        days.append(
            {
                "date": current_day,
                "status": status,
                "color": color,
                "hours": hours,
                "is_today": current_day == timezone.localdate(),
                "is_holiday": is_holiday,
                "weekday": current_day.weekday(),
                "holiday_name": holiday_description,
            }
        )

        current_day += timedelta(days=1)

    first_weekday = (start_date.weekday() + 1) % 7
    blank_days = [None] * first_weekday

    weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month_num = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    context = {
        "days": days,
        "month": start_date.strftime("%B %Y"),
        "blank_days": blank_days,
        "weekdays": weekdays,
        "total_hours": total_hours,
        "total_minutes": total_minutes,
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month_num,
        "today": date.today(),
    }

    return render(request, "calendar.html", context)


def holiday_list(request):
    current_year = date.today().year

    if request.method == "POST":
        date_value = request.POST.get("date")
        description = request.POST.get("description")

        if not date_value or not description:
            messages.error(request, "Please fill in all fields.")
        else:
            year = date.fromisoformat(date_value).year
            if Holiday.objects.filter(date=date_value).exists():
                messages.warning(request, "Holiday already exists for this date.")
            else:
                Holiday.objects.create(
                    date=date_value, description=description, year=year
                )
                messages.success(request, "Holiday added successfully!")

        return redirect("holiday_list")

    holidays = Holiday.objects.filter(year=current_year).order_by("date")
    return render(
        request,
        "employee_portal/holiday_list.html",
        {"holidays": holidays, "year": current_year},
    )


def check_today_holiday(request):
    today = date.today()
    holiday = Holiday.objects.filter(date=today).first()
    if holiday:
        return JsonResponse({"is_holiday": True, "description": holiday.description})
    else:
        return JsonResponse({"is_holiday": False})
