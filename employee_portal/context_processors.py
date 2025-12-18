from .models import Employee

def employee_context(request):
    if request.user.is_authenticated:
        emp = Employee.objects.filter(user=request.user).first()
        return {'emp': emp}
    return {}