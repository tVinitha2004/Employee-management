from django import forms
from .models import Employee


class CandidateForm(forms.ModelForm):
    current_salary = forms.DecimalField(required=False)


class Product_Form(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"
