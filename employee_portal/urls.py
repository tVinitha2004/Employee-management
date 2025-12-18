from django.urls import path
from . import views


urlpatterns = [
    path("home/", views.dashboard, name="dashboard"),
    path("onboarding/candidate/", views.employee_list, name="employee_list"),
    # path('add/', views.add_candidate, name='add_candidate'),
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
    # path("manage-titles/", views.manage_titles, name="manage_titles"),
    # path("delete-title/<int:pk>/", views.delete_title, name="delete_title"),
    # path("edit-title/<int:pk>/", views.edit_title, name="edit_title"),
]
