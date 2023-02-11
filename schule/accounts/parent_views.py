from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import *
from accounts.forms import *
from accounts.decorators import parent_only
from .helper_functions import *

@login_required(login_url='login')
@parent_only
def parent_grades(request):
    parent = Parent.objects.get(user=request.user)
    student = parent.child

    context = {
        'parent': parent,
        'student': student,
        'student_grades': get_student_grades(student),
    }

    return render(request, "accounts/grades.html", context)

@login_required(login_url='login')
@parent_only
def parent_absences(request):
    parent = Parent.objects.get(user=request.user)
    student = parent.child

    context ={
        'parent': parent,
        'student': student,
        'absences': get_student_absences(student)
    }
    return render(request, "accounts/absences.html", context)

@login_required(login_url='login')
@parent_only
def parent_remarks(request):
    parent = Parent.objects.get(user=request.user)
    student = parent.child

    context ={
        'parent': parent,
        'student': student,
        'remarks': get_student_remarks(student)
    }
    return render(request, "accounts/remarks.html", context)

@login_required(login_url='login')
@parent_only
def parent_praises(request):
    parent = Parent.objects.get(user=request.user)
    student = parent.child

    context ={
        'parent': parent,
        'student': student,
        'praises': get_student_praises(student)
    }
    return render(request, "accounts/praises.html", context)