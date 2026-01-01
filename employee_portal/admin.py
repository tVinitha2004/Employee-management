from django.contrib import admin
from .models import Employee, Attendance, Holiday, Designation, Task, Leave

admin.site.register(Employee)
admin.site.register(Attendance)


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ("employee", "start_date", "end_date", "total_days")


@admin.register(Task)
class Task(admin.ModelAdmin):
    list_display = (
        "title",
        "assigned_to_id",
        "status",
        "worked_hours",
        "created_at",
    )
    readonly_fields = ("created_at",)


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ("date", "description", "year")
    list_filter = ("year",)


admin.site.register(Designation)
