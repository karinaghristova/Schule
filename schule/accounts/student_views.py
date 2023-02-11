from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import *
from accounts.forms import *
from accounts.decorators import student_only
from .helper_functions import *

@login_required(login_url='login')
@student_only
def student_update_info(request):
    student = Student.objects.get(user=request.user)
    form = StudentUpdateForStudentsForm(instance=student)
    if request.method == "POST":
        form = StudentUpdateForStudentsForm(request.POST, instance=student)
        if form.is_valid():
            user = student.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            form.save()
            return redirect("home")

    context = {'form': form}
    return render(request, 'accounts/student/student_update_form.html', context)

@login_required(login_url='login')
@student_only
def student_account(request):
    student = Student.objects.get(user=request.user)
    context = {'student': student,}
    return render(request, 'accounts/student/student_account.html', context)

@login_required(login_url='login')
@student_only
def student_grades(request):
    student = Student.objects.get(user=request.user)

    context = {
        'student': student,
        'student_grades': get_student_grades(student),
        'average_grade_winter_term': get_average_grade_for_term_of_student(student, 'winter'),
        'average_grade_summer_term': get_average_grade_for_term_of_student(student, 'summer'),
        'average_grade': get_average_grade_of_student(student),
        'failure_grades_winter': get_count_of_grades_by_value_and_term(student, 2, 'winter'),
        'failure_grades_summer': get_count_of_grades_by_value_and_term(student, 2, 'summer'),
        'passing_grades_winter': get_count_of_grades_by_value_and_term(student, 3, 'winter'),
        'passing_grades_summer': get_count_of_grades_by_value_and_term(student, 3, 'summer'),
        'good_grades_winter': get_count_of_grades_by_value_and_term(student, 4, 'winter'),
        'good_grades_summer': get_count_of_grades_by_value_and_term(student, 4, 'summer'),
        'very_good_grades_winter': get_count_of_grades_by_value_and_term(student, 5, 'winter'),
        'very_good_grades_summer': get_count_of_grades_by_value_and_term(student, 5, 'summer'),
        'excellent_grades_winter': get_count_of_grades_by_value_and_term(student, 6, 'winter'),
        'excellent_grades_summer': get_count_of_grades_by_value_and_term(student, 6, 'summer'),
    }

    return render(request, "accounts/grades.html", context)

@login_required(login_url='login')
@student_only
def student_absences(request):
    student = Student.objects.get(user=request.user)

    context ={
        'student': student,
        'absences': get_student_absences(student),
        'absences_winter': get_student_absences_for_term(student, 'winter'),
        'absences_summer': get_student_absences_for_term(student, 'summer'),
    }
    return render(request, "accounts/absences.html", context)

@login_required(login_url='login')
@student_only
def student_remarks(request):
    student = Student.objects.get(user=request.user)

    context ={
        'student': student,
        'remarks': get_student_remarks(student),
        'remarks_winter': get_student_remarks_for_term(student, 'winter'),
        'remarks_summer': get_student_remarks_for_term(student, 'summer'),
    }
    return render(request, "accounts/remarks.html", context)

@login_required(login_url='login')
@student_only
def student_praises(request):
    student = Student.objects.get(user=request.user)

    context ={
        'student': student,
        'praises': get_student_praises(student),
        'praises_winter': get_count_of_student_praises_for_term(student, 'winter'),
        'praises_summer': get_count_of_student_praises_for_term(student, 'summer'),
    }
    return render(request, "accounts/praises.html", context)