from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from employee_portal.models import Employee


def LoginPage(request):
    if request.user.is_authenticated:
        return redirect("main/home")

    if request.method == "POST":
        email = request.POST.get("username").strip()
        password = request.POST.get("password").strip()

        # Find username using email
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            username = email 

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("main/home")
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, "login.html")
    if request.method == "POST":
            print("Form submitted")
            print(request.POST)
            print("User object:", user)

    return render(request, "login.html")


# logout
def LogoutUser(request):

    logout(request)

    return redirect("/")


  

def EmployeeSignupView(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    context = {'email': employee.official_email}

    if request.method == "POST":
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        if password != confirm:
            context["error"] = "Passwords do not match!"
            return render(request, "employee_signup.html", context)

        # Get or create user
        user = User.objects.filter(username=employee.official_email).first()
        if user:
            user.set_password(password)  # Update password
            user.save()
        else:
            user = User.objects.create_user(
                username=employee.official_email,
                password=password,
                email=employee.official_email,
                first_name=employee.first_name,
                last_name=employee.last_name
            )

        # Link employee to user
        if not employee.user:
            employee.user = user
            employee.save()

        # Auto-login after signup
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect("/")

    return render(request, "employee_signup.html", context)

