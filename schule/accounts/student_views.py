from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import *
from accounts.forms import *
from accounts.decorators import student_only
from .helper_functions import *

@login_required(login_url='login')
@student_only
def student_grades(request):
    student = Student.objects.get(user=request.user)

    context = {
        'student': student,
        'student_grades': get_student_grades(student),
    }

    return render(request, "accounts/grades.html", context)

@login_required(login_url='login')
@student_only
def student_absences(request):
    student = Student.objects.get(user=request.user)

    context ={
        'student': student,
        'absences': get_student_absences(student)
    }
    return render(request, "accounts/absences.html", context)

@login_required(login_url='login')
@student_only
def student_remarks(request):
    student = Student.objects.get(user=request.user)

    context ={
        'student': student,
        'remarks': get_student_remarks(student)
    }
    return render(request, "accounts/remarks.html", context)

@login_required(login_url='login')
@student_only
def student_praises(request):
    student = Student.objects.get(user=request.user)

    context ={
        'student': student,
        'praises': get_student_praises(student)
    }
    return render(request, "accounts/praises.html", context)