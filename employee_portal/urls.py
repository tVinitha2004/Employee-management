from django.urls import path
from . import views


urlpatterns = [
    path("home/", views.dashboard, name="dashboard"),
    path("onboarding/candidate/", views.employee_list, name="employee_list"),
    path("employee/edit/<int:emp_id>/", views.edit_employee, name="edit_employee"),
    path(
        "employee/<int:emp_id>/delete/", views.delete_employee, name="delete_employee"
    ),
    path("home/my-space/overview/", views.myspace_overview, name="myspace_overview"),
    path("toggle-check/", views.toggle_check, name="toggle_check"),
    path("attendance-calendar/", views.attendance_calendar, name="attendance_calendar"),
    path("check-browser-close/", views.check_browser_close, name="check_browser_close"),
    path("my-account/", views.my_account, name="my_account"),
    path("holidays/", views.holiday_list, name="holiday_list"),
    path("api/check-holiday/", views.check_today_holiday, name="check_today_holiday"),
    path(
        "holiday/delete/<int:holiday_id>/", views.delete_holiday, name="delete_holiday"
    ),
    path("change-password/", views.change_password, name="change_password"),
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/add/", views.add_task, name="add_task"),
    path("tasks/view/<int:id>/", views.task_view, name="task_view"),
    path("tasks/edit/<int:id>/", views.task_edit, name="task_edit"),
    path("tasks/delete/<int:id>/", views.task_delete, name="task_delete"),
    path("leave-list/", views.leave_list, name="leave_list"),
    path("leave/add/", views.add_leave, name="add_leave"),
    path("leave/edit/<int:leave_id>/", views.edit_leave, name="edit_leave"),
    path("leave/delete/<int:leave_id>/", views.delete_leave, name="delete_leave"),
]
