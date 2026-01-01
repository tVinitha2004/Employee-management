# def is_admin_user(user):
#     if not user.is_authenticated:
#         return False


#     if user.is_superuser:
#         return True


#     if hasattr(user, "employee") and user.employee.role == "admin":
#         return True

#     return False


# def is_admin_user(user):
#     return user.is_authenticated and (
#         user.is_superuser
#         or (hasattr(user, "employee") and user.employee.role == "admin")
#     )
