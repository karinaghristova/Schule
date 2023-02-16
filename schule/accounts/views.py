from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django import forms

from .models import *
from .forms import *
from .decorators import *
# Create your views here.

from .teacher_views import *
from .parent_views import *
from .student_views import *


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            role = form.cleaned_data.get('role')
            school_name = form.cleaned_data.get('school_name')

            group = Group.objects.get(name=role)
            user.groups.add(group)

            school = School.objects.get(name=school_name)

            if role == 'student':
                Student.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    school=school,
                )
            elif role == 'parent':
                Parent.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    school=school,
                )

            return redirect('home')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def registerPageTeacher(request):
    form = CreateUserFormTeacher()

    if request.method == "POST":
        form = CreateUserFormTeacher(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')

            group = Group.objects.get(name='teacher')
            user.groups.add(group)

            Teacher.objects.create(
                user=user,
                email=email,
                first_name=first_name,
                last_name=last_name
            )

            return redirect('home')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect.')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect("login")


def __get_context_for_admin_homepage__():
    teachers_count = Teacher.objects.all().count()
    students_count = Student.objects.all().count()
    parents_count = Parent.objects.all().count()

    cities_count = City.objects.all().count()
    schools_count = School.objects.all().count()

    grades_count_winter = Grade.objects.all().filter(
        term__name__contains="winter").count()
    grades_count_summer = Grade.objects.all().filter(
        term__name__contains="summer").count()

    absences_count_winter = Absence.objects.all().filter(
        term__name__contains="winter").count()
    absences_count_summer = Absence.objects.all().filter(
        term__name__contains="summer").count()

    remarks_count_winter = Remark.objects.all().filter(
        term__name__contains="winter").count()
    remarks_count_summer = Remark.objects.all().filter(
        term__name__contains="summer").count()

    praises_count_winter = Praise.objects.all().filter(
        term__name__contains="winter").count()
    praises_count_summer = Praise.objects.all().filter(
        term__name__contains="summer").count()
    context = {
        'teachers_count': teachers_count,
        'students_count': students_count,
        'parents_count': parents_count,
        'cities_count': cities_count,
        'schools_count': schools_count,
        'grades_count': grades_count_winter + grades_count_summer,
        'grades_count_winter': grades_count_winter,
        'grades_count_summer': grades_count_summer,
        'absences_count': absences_count_winter + absences_count_summer,
        'absences_count_winter': absences_count_winter,
        'absences_count_summer': absences_count_summer,
        'remarks_count': remarks_count_winter + remarks_count_summer,
        'remarks_count_winter': remarks_count_winter,
        'remarks_count_summer': remarks_count_summer,
        'praises_count': praises_count_winter + praises_count_summer,
        'praises_count_winter': praises_count_winter,
        'praises_count_summer': praises_count_summer,
    }
    return context


def __get_context_for_teacher_homepage__(teacher):
    school = teacher.school
    students_in_school_count = Student.objects.all().filter(school=school).count()
    parents_in_school_count = Parent.objects.all().filter(school=school).count()
    grades_in_school_count = Grade.objects.all().count()
    grades_in_school_written_by_teacher = Grade.objects.all().filter(
        subject_class__teacher=teacher).count()
    failure_grades_written_by_teacher = Grade.objects.all().filter(
        subject_class__teacher=teacher, number=2).count()
    passing_grades_written_by_teacher = Grade.objects.all().filter(
        subject_class__teacher=teacher, number=3).count()
    good_grades_written_by_teacher = Grade.objects.all().filter(
        subject_class__teacher=teacher, number=4).count()
    very_good_grades_written_by_teacher = Grade.objects.all().filter(
        subject_class__teacher=teacher, number=5).count()
    excellent_grades_written_by_teacher = Grade.objects.all().filter(
        subject_class__teacher=teacher, number=6).count()
    absences_in_school_count = Absence.objects.all().filter(
        student__school=school).count()
    absences_in_school_written_by_teacher_count = Absence.objects.all().filter(
        subject_class__teacher=teacher).count()
    remarks_in_school_count = Remark.objects.all().filter(
        student__school=school).count()
    remarks_in_school_written_by_teacher = Remark.objects.all().filter(
        teacher=teacher).count()
    praises_in_school_count = Praise.objects.all().filter(
        student__school=school).count()
    praises_in_school_written_by_teacher = Praise.objects.all().filter(
        teacher=teacher).count()

    context = {
        'school': school.name,
        'students_in_school_count': students_in_school_count,
        'parents_in_school_count': parents_in_school_count,
        'grades_in_school_count': grades_in_school_count,
        'grades_in_school_written_by_teacher': grades_in_school_written_by_teacher,
        'failure_grades_written_by_teacher': failure_grades_written_by_teacher,
        'passing_grades_written_by_teacher': passing_grades_written_by_teacher,
        'good_grades_written_by_teacher': good_grades_written_by_teacher,
        'very_good_grades_written_by_teacher': very_good_grades_written_by_teacher,
        'excellent_grades_written_by_teacher': excellent_grades_written_by_teacher,
        'absences_in_school_count': absences_in_school_count,
        'absences_in_school_written_by_teacher_count': absences_in_school_written_by_teacher_count,
        'remarks_in_school_count': remarks_in_school_count,
        'remarks_in_school_written_by_teacher': remarks_in_school_written_by_teacher,
        'praises_in_school_count': praises_in_school_count,
        'praises_in_school_written_by_teacher': praises_in_school_written_by_teacher,
    }
    return context


def __get_additional_context_for_parents_and_students_homepage__(student):
    context = {
        'grades_count': get_count_of_grades_for_student(student),
        'grades_count_winter': get_count_of_grades_by_term(student, 'winter'),
        'grades_count_summer': get_count_of_grades_by_term(student, 'summer'),
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
        'absences': get_count_of_student_absences(student),
        'absences_winter': get_count_of_student_absences_for_term(student, 'winter'),
        'absences_summer': get_count_of_student_absences_for_term(student, 'summer'),
        'remarks': get_count_of_student_remarks(student),
        'remarks_winter': get_count_of_student_remarks_for_term(student, 'winter'),
        'remarks_summer': get_count_of_student_remarks_for_term(student, 'summer'),
        'praises': get_count_of_student_praises(student),
        'praises_winter': get_count_of_student_praises_for_term(student, 'winter'),
        'praises_summer': get_count_of_student_praises_for_term(student, 'summer'),
    }
    return context

def __get_context_for_parent_homepage__(parent):
    has_child = parent.child
    if has_child:
        student = parent.child
        context = {
            'parent': parent,
            'has_child': has_child,
            'student': student,
        }
        additional_context = __get_additional_context_for_parents_and_students_homepage__(parent.child)
        context.update(additional_context)
    else:
        context = {
            'parent': parent,
            'has_child': has_child,
        }
    return context


def __get_context_for_student_homepage__(student):
    context = {
        'student': student,
    }
    additional_context = __get_additional_context_for_parents_and_students_homepage__(student)
    context.update(additional_context)

    return context


@login_required(login_url='login')
@allow_users(allowed_roles=['admin', 'teacher', 'parent', 'student'])
def home(request):
    if request.user.is_staff:
        context = __get_context_for_admin_homepage__()
        return render(request, 'accounts/homepage_admin.html', context)

    if request.user.groups.filter(name='teacher').exists():
        teacher = Teacher.objects.get(user=request.user)
        context = __get_context_for_teacher_homepage__(teacher)
        return render(request, 'accounts/homepage_teacher.html', context)

    if request.user.groups.filter(name='student').exists():
        student = Student.objects.get(user=request.user)
        context = __get_context_for_student_homepage__(student)
        return render(request, 'accounts/homepage_student.html', context)

    if request.user.groups.filter(name='parent').exists():
        parent = Parent.objects.get(user=request.user)
        context = __get_context_for_parent_homepage__(parent)
        return render(request, 'accounts/homepage_parent.html', context)
