from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError


class Designation(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("employee", "Employee"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="employee")
    DESIGNATION_CHOICES = [
        ("CEO", "CEO"),
        ("Administration", "Administration"),
        ("Manager", "Manager"),
        ("Assistant Manager", "Assistant Manager"),
        ("Team Member", "Team Member"),
        ("Managing Director", "Managing Director"),
        ("Chief Executive Officer", "Chief Executive Officer"),
        ("Software Engineer", "Software Engineer"),
        ("Web Developer", "Web Developer"),
        ("Frontend Developer", "Frontend Developer"),
        ("Backend Developer", "Backend Developer"),
        ("Full Stack Developer", "Full Stack Developer"),
        ("Team Lead", "Team Lead"),
        ("Technical Lead", "Technical Lead"),
        ("Senior Manager", "Senior Manager"),
        ("Consultant", "Consultant"),
        ("Junior Developer", "Junior Developer"),
        ("Trainee", "Trainee"),
        ("Intern", "Intern"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    check_in_status = models.BooleanField(default=False)

    # candidate details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    official_email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    # dob
    dob = models.DateField(blank=True, null=True)
    uan_number = models.CharField(max_length=20, blank=True, null=True)
    aadhaar_number = models.CharField(max_length=20, blank=True, null=True)
    pan_number = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(upload_to="employee_photos/", blank=True, null=True)

    # address details
    present_address_line1 = models.CharField(max_length=255, blank=True, null=True)
    present_address_line2 = models.CharField(max_length=255, blank=True, null=True)
    present_city = models.CharField(max_length=100, blank=True, null=True)
    present_state = models.CharField(max_length=100, blank=True, null=True)
    present_country = models.CharField(max_length=100, blank=True, null=True)
    present_postal_code = models.CharField(max_length=20, blank=True, null=True)

    permanent_same_as_present = models.BooleanField(
        default=False, null=True, blank=True
    )
    permanent_address_line1 = models.CharField(max_length=255, blank=True, null=True)
    permanent_address_line2 = models.CharField(max_length=255, blank=True, null=True)
    permanent_city = models.CharField(max_length=100, blank=True, null=True)
    permanent_state = models.CharField(max_length=100, blank=True, null=True)
    permanent_country = models.CharField(max_length=100, blank=True, null=True)
    permanent_postal_code = models.CharField(max_length=20, blank=True, null=True)
    source_of_hire = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    # Professional Details
    experience = models.CharField(max_length=100, blank=True, null=True)
    skill_set = models.CharField(max_length=255, blank=True, null=True)
    highest_qualification = models.CharField(max_length=100, blank=True, null=True)
    additional_information = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=DESIGNATION_CHOICES,
        default="Team Member",
    )
    current_salary = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    offer_letter = models.FileField(upload_to="offer_letters/", blank=True, null=True)
    tentative_joining_date = models.DateField(blank=True, null=True)

    # education
    college_name = models.CharField(max_length=255, null=True, blank=True)
    degree = models.CharField(max_length=255, null=True, blank=True)
    field_of_study = models.CharField(max_length=255, null=True, blank=True)
    year_of_completion = models.CharField(max_length=50, null=True, blank=True)

    # Work Experience
    occupation = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    currently_work_here = models.CharField(max_length=10, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # If the Employee is linked to a User
        if self.user:
            if self.title == "CEO":
                self.user.is_superuser = True
                self.user.is_staff = True
            else:
                self.user.is_superuser = False
                self.user.is_staff = False
            self.user.save()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(default=0)  # total seconds checked-in
    last_active = models.DateTimeField(null=True, blank=True)
    eight_hours_completed = models.BooleanField(default=False)
    is_running = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    def get_status(self):
        # If user has checked in/out
        if self.check_in and self.check_out:
            check_in_str = self.check_in.strftime("%I:%M %p")
            check_out_str = self.check_out.strftime("%I:%M %p")
            return f"{check_in_str} - {check_out_str}"

        # Weekend without check-in
        if self.date.weekday() >= 5:
            return "Weekend"

        # Absent
        return "Absent"


class Holiday(models.Model):
    date = models.DateField(unique=True)
    description = models.CharField(max_length=255)
    year = models.IntegerField()

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.date} - {self.description}"


class Task(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="task_images/", blank=True, null=True)

    assigned_to = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="tasks"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    worked_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def worked_hours_display(self):
        hours = int(self.worked_hours)
        minutes = int((self.worked_hours - hours) * 60)
        return f"{hours}:{minutes:02d}"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.worked_hours > 4:
            raise ValidationError("Maximum 4 hours only can select")

        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError("End date cannot be before start date")

    def __str__(self):
        return self.title


class Leave(models.Model):
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    command = models.TextField(blank=True, null=True)
    total_days = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_name} ({self.start_date} to {self.end_date})"
