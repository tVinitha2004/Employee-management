from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Employee, Task
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Attendance
from django.http import JsonResponse
from datetime import date, timedelta, time
from calendar import monthrange
from django.db.models import Sum
from django.contrib import messages
from django.contrib import admin
from .models import Holiday
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError


@login_required
def change_password(request):
    user = request.user

    if request.method == "POST":
        current = request.POST.get("current_password")
        new = request.POST.get("new_password")
        confirm = request.POST.get("confirm_password")

        if not user.check_password(current):
            messages.error(
                request, "Current password is incorrect.", extra_tags="password"
            )
            return render(request, "my_account.html", {"emp": user.employee})

        if new != confirm:
            messages.error(request, "Passwords do not match.", extra_tags="password")
            return render(request, "my_account.html", {"emp": user.employee})

        user.set_password(new)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(
            request, "Password changed successfully.", extra_tags="password_msg"
        )
        return render(request, "my_account.html", {"emp": user.employee})


@login_required
def my_account(request):
    user = request.user
    emp = Employee.objects.filter(user=user).first()
    return render(
        request,
        "my_account.html",
        {
            "user": user,
            "emp": emp,
            "designations": Employee.DESIGNATION_CHOICES,
        },
    )


def generate_password(first_name, dob):
    """
    first 4 letters of first name (CAPS) + DOB (YYYYMMDD)
    """
    name_part = (first_name[:4]).upper()

    if isinstance(dob, str):
        dob = datetime.strptime(dob, "%Y-%m-%d").date()

    dob_part = dob.strftime("%Y%m%d")

    return f"{name_part}{dob_part}"


def employee_list(request):

    if request.method == "POST":
        # Get data from form
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        official_email = request.POST.get("official_email")
        if official_email:
            official_email = official_email.strip().lower()
        phone = request.POST.get("phone")
        dob = request.POST.get("dob")

        if dob:
            try:
                dob = datetime.strptime(dob, "%Y-%m-%d").date()
            except ValueError:
                dob = None
        else:
            dob = None

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
        offer_letter = request.FILES.get("offer_letter")

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

        raw_password = generate_password(first_name, dob)

        #  create user
        user, created = User.objects.get_or_create(
            username=official_email,
            first_name=first_name,
            last_name=last_name,
            email=official_email,
            is_staff=False,
        )
        user.set_password(raw_password)
        user.save()

        if user.is_superuser:
            title = "CEO"
        else:
            title = title or "Team Member"

        title = "CEO" if user.is_superuser else (title or "Team Member")

        if permanent_same_as_present:
            permanent_address_line1 = present_address_line1
            permanent_address_line2 = present_address_line2
            permanent_city = present_city
            permanent_state = present_state
            permanent_country = present_country
            permanent_postal_code = present_postal_code

        # Create Employee
        Employee.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            official_email=official_email,
            phone=phone,
            dob=dob,
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
        messages.success(
            request,
            f"Employee created successfully. Temporary password: {raw_password}",
        )

        return redirect("employee_list")

    # GET request
    employees = Employee.objects.all()
    paginator = Paginator(employees, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "employee_portal/employee_list.html",
        {
            "employees": employees,
            "designations": Employee.DESIGNATION_CHOICES,
        },
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
        dob = request.POST.get("dob")

        if dob:
            try:
                emp.dob = datetime.strptime(dob, "%Y-%m-%d").date()
            except ValueError:
                pass

        emp.uan_number = request.POST.get("uan_number")
        emp.aadhaar_number = request.POST.get("aadhaar_number")
        emp.pan_number = request.POST.get("pan_number")

        if request.POST.get("remove_photo"):
            if emp.photo:
                emp.photo.delete(save=False)
                emp.photo = None
        # If a new photo is uploaded, update
        if request.FILES.get("photo"):
            emp.photo = request.FILES.get("photo")

        # Address details

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
        employee.user.delete()

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


def toggle_check(request):

    user = request.user
    today = timezone.localdate()
    leave_today = Leave.objects.filter(
        employee_id=request.user.employee.id, start_date__lte=today, end_date__gte=today
    ).exists()

    if today.weekday() == 6 or today.weekday() == 5:
        messages.error(request, "Weekends are holiday so no need to check-in.")
        return render(request, "calendar.html")

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
    now = timezone.now()

    running_attendance = Attendance.objects.filter(
        user=request.user, start_time__isnull=False, check_out__isnull=True
    ).first()

    # If the user has a running attendance from today
    if running_attendance:
        midnight = timezone.make_aware(
            datetime.combine(running_attendance.date + timedelta(days=1), time.min)
        )

        if now >= midnight:
            elapsed = (midnight - running_attendance.start_time).total_seconds()
            running_attendance.duration_seconds += int(elapsed)
            running_attendance.check_out = midnight.time()
            running_attendance.start_time = None
            running_attendance.is_running = False
            running_attendance.save()

    # --------------- GET ----------------
    if request.method == "GET":
        total = attendance.duration_seconds or 0

        # If session is running, use start_time (datetime) to compute elapsed
        if attendance.start_time and not attendance.check_out:
            elapsed = (timezone.now() - attendance.start_time).total_seconds()
            total += int(elapsed)

        # 8 hours condition
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
                "is_leave_day": leave_today,
            }
        )

    # --------------- POST ----------------

    if request.method == "POST":
        action = request.POST.get("action")

        # CHECK-IN
        if action in ("checkin", "check_in"):
            if leave_today:
                return JsonResponse(
                    {"error": "Leave day. Cannot check-in."}, status=400
                )
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

        # CHECK-OUT
        if action in ("checkout", "check_out"):
            now = timezone.now()

            if attendance.start_time:
                elapsed = (now - attendance.start_time).total_seconds()
                attendance.duration_seconds += int(elapsed)  # <— FIXED (accurate)

            # 8 hours
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

        # PAUSE
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

    # superuser condition
    selected_user_id = request.GET.get("user_id")
    if request.user.is_superuser and selected_user_id:
        selected_user = User.objects.filter(id=selected_user_id).first()
    else:
        selected_user = request.user

    start_date = date(year, month, 1)
    from .models import Employee

    all_employees = (
        Employee.objects.select_related("user").all()
        if request.user.is_superuser
        else None
    )

    # Handle December January transition
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)

    end_date = next_month - timedelta(days=1)

    emp = Employee.objects.filter(user=selected_user).first()

    days = []
    current_day = start_date

    # Holidays
    from .models import Holiday

    holidays = {h.date: h.description for h in Holiday.objects.filter(date__year=year)}

    # Leaves
    leaves = Leave.objects.filter(
        employee=emp, start_date__lte=end_date, end_date__gte=start_date
    )

    leave_dates = set()
    for leave in leaves:
        d = leave.start_date
        while d <= leave.end_date:
            leave_dates.add(d)
            d += timedelta(days=1)

    # Total working hours
    total_seconds = (
        Attendance.objects.filter(
            user=selected_user, date__year=year, date__month=month
        )
        .exclude(date__in=holidays.keys())
        .aggregate(Sum("duration_seconds"))["duration_seconds__sum"]
        or 0
    )
    # --- TASK HOURS ONLY IN END DATE MONTH ---
    tasks = Task.objects.filter(
        assigned_to=emp, end_date__year=year, end_date__month=month
    )

    total_task_hours = 0

    for task in tasks:
        if task.worked_hours:
            total_task_hours += float(task.worked_hours)

    # Convert to hours/minutes
    task_hours = int(total_task_hours)
    task_minutes = int((total_task_hours - task_hours) * 60)

    total_hours = total_seconds // 3600
    total_minutes = (total_seconds % 3600) // 60

    joining_date = emp.tentative_joining_date if emp else None

    while current_day <= end_date:
        attendance = Attendance.objects.filter(
            user=selected_user, date=current_day
        ).first()

        holiday_description = None

        # DEFAULT
        status = "Absent"
        color = "red"
        hours = None
        can_apply_leave = True

        #  LEAVE
        if current_day in leave_dates:
            status = "Leave"
            color = "blue"

        # HOLIDAY
        elif current_day in holidays:
            status = "Holiday"
            color = "yellow"
            holiday_description = holidays[current_day]

        # BEFORE JOINING DATE
        elif joining_date and current_day < joining_date:
            status = ""
            color = ""

        # PRESENT
        elif attendance and attendance.duration_seconds > 0:
            h = attendance.duration_seconds // 3600
            m = (attendance.duration_seconds % 3600) // 60
            hours = f"{h:02d}:{m:02d}"
            status = "Present"
            color = "green"

        days.append(
            {
                "date": current_day,
                "status": status,
                "color": color,
                "hours": hours,
                "is_today": current_day == timezone.localdate(),
                "is_holiday": current_day in holidays,
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
    all_employees = (
        Employee.objects.select_related("user").all()
        if request.user.is_superuser
        else None
    )

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
        "all_employees": all_employees,
        "selected_user": selected_user,
        "task_hours": task_hours,
        "task_minutes": task_minutes,
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


def delete_holiday(request, holiday_id):
    holiday = get_object_or_404(Holiday, id=holiday_id)

    if request.method == "POST":
        holiday.delete()
        messages.success(request, "Holiday deleted successfully!")

    return redirect("holiday_list")


def check_today_holiday(request):
    today = date.today()
    holiday = Holiday.objects.filter(date=today).first()
    if holiday:
        return JsonResponse({"is_holiday": True, "description": holiday.description})
    else:
        return JsonResponse({"is_holiday": False})


@login_required
def task_list(request):
    filter_type = request.GET.get("filter", "all")  # default = all

    if filter_type == "my":
        # Current user oda tasks
        tasks = Task.objects.filter(assigned_to__user=request.user).order_by("-id")
    else:
        # All tasks
        tasks = Task.objects.select_related("assigned_to").all().order_by("-id")

    context = {
        "tasks": tasks,
        "filter_type": filter_type,
    }
    return render(request, "tasks/task_list.html", context)


@login_required
def add_task(request):
    employees = Employee.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        status = request.POST.get("status")
        worked_hours = request.POST.get("worked_hours") or 0
        assigned_to_id = request.POST.get("assigned_to")
        image = request.FILES.get("image")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        # assigned_employee = Employee.objects.get(id=assigned_to_id)
        if not start_date or not end_date:
            messages.error(
                request, "Start date and End date are required", extra_tags="task"
            )
            return redirect("add_task")

        Task.objects.create(
            title=title,
            description=description,
            image=image,
            assigned_to_id=assigned_to_id,
            status=status,
            worked_hours=worked_hours,
            start_date=start_date,
            end_date=end_date,
        )

        messages.success(request, "Task added successfully ")
        return redirect("task_list")

    return render(request, "tasks/add_task.html", {"employees": employees})


# @login_required
# def add_task(request):
#     employees = Employee.objects.all()

#     if request.method == "POST":
#         try:
#             task = Task(
#                 title=request.POST.get("title"),
#                 description=request.POST.get("description"),
#                 status=request.POST.get("status"),
#                 worked_hours=request.POST.get("worked_hours") or 0,
#                 assigned_to_id=request.POST.get("assigned_to"),
#                 image=request.FILES.get("image"),
#                 start_date=request.POST.get("start_date"),
#                 end_date=request.POST.get("end_date"),
#             )

#             task.full_clean()
#             task.save()

#             messages.success(request, "Task added successfully")
#             return redirect("task_list")

#         except ValidationError as e:
#             for msg in e.messages:
#                 messages.error(request, msg)

#     return render(request, "tasks/add_task.html", {"employees": employees})


@login_required
def task_view(request, id):
    task = get_object_or_404(Task, id=id)
    return render(request, "tasks/task_view.html", {"task": task})


@login_required
def task_edit(request, id):
    task = Task.objects.get(id=id)
    employees = Employee.objects.all()

    if request.method == "POST":
        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        task.status = request.POST.get("status")
        task.worked_hours = request.POST.get("worked_hours")
        task.start_date = request.POST.get("start_date")
        task.end_date = request.POST.get("end_date")

        assigned_to_id = request.POST.get("assigned_to")
        task.assigned_to = Employee.objects.get(id=assigned_to_id)
        if request.FILES.get("image"):
            task.image = request.FILES.get("image")

        if request.FILES.get("image"):
            task.image = request.FILES.get("image")

        task.save()
        return redirect("task_list")

    return render(
        request,
        "tasks/add_task.html",
        {"task": task, "employees": employees, "is_edit": True},
    )


@login_required
def task_delete(request, id):
    Task.objects.filter(id=id).delete()
    return redirect("task_list")


from .models import Leave, Employee, Holiday


@login_required
def add_leave(request):
    employee = Employee.objects.get(user=request.user)

    if request.method == "POST":
        start_date = datetime.strptime(
            request.POST.get("start_date"), "%Y-%m-%d"
        ).date()

        end_date = datetime.strptime(request.POST.get("end_date"), "%Y-%m-%d").date()

        command = request.POST.get("command")

        total_days = calculate_leave_days(start_date, end_date)

        Leave.objects.create(
            employee=employee,
            start_date=start_date,
            end_date=end_date,
            command=command,
            total_days=total_days,
        )

        return redirect("leave_list")

    return render(request, "leave/add_leave.html")


@login_required
def leave_list(request):
    employee = Employee.objects.get(user=request.user)
    leaves = Leave.objects.filter(employee=employee)
    return render(request, "leave/leave_list.html", {"leaves": leaves})


@login_required
def edit_leave(request, leave_id):
    employee = Employee.objects.get(user=request.user)
    leave = get_object_or_404(Leave, id=leave_id, employee=employee)

    if request.method == "POST":
        leave.start_date = datetime.strptime(
            request.POST.get("start_date"), "%Y-%m-%d"
        ).date()
        leave.end_date = datetime.strptime(
            request.POST.get("end_date"), "%Y-%m-%d"
        ).date()
        leave.command = request.POST.get("command")
        leave.total_days = calculate_leave_days(leave.start_date, leave.end_date)
        leave.save()
        messages.success(request, "Leave updated successfully")
        return redirect("leave_list")

    # Pass leave to template
    return render(request, "leave/add_leave.html", {"leave": leave})


@login_required
def delete_leave(request, leave_id):
    employee = Employee.objects.filter(user=request.user).first()
    if not employee:
        messages.error(request, "Access denied")
        return redirect("leave_list")

    leave = get_object_or_404(Leave, id=leave_id, employee=employee)

    leave.delete()
    messages.success(request, "Leave deleted successfully")
    return redirect("leave_list")


def calculate_leave_days(start_date, end_date):

    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    total_days = 0

    # holidays list
    holidays = Holiday.objects.values_list("date", flat=True)

    current_date = start_date
    while current_date <= end_date:
        # weekday(): Monday=0 ... Sunday=6
        if current_date.weekday() not in (5, 6) and current_date not in holidays:
            total_days += 1

        current_date += timedelta(days=1)

    return total_days
