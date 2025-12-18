from django.contrib import admin
from .models import Employee, Attendance, Holiday, Designation

admin.site.register(Employee)
admin.site.register(Attendance)


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ("date", "description", "year")
    list_filter = ("year",)


admin.site.register(Designation)
