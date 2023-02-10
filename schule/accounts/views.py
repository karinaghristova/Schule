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
    grades_in_school_written_by_teacher = Grade.objects.all().filter(subject_class__teacher=teacher).count()
    failure_grades_written_by_teacher = Grade.objects.all().filter(subject_class__teacher=teacher, number=2).count()
    passing_grades_written_by_teacher = Grade.objects.all().filter(subject_class__teacher=teacher, number=3).count()
    good_grades_written_by_teacher = Grade.objects.all().filter(subject_class__teacher=teacher, number=4).count()
    very_good_grades_written_by_teacher = Grade.objects.all().filter(subject_class__teacher=teacher, number=5).count()
    excellent_grades_written_by_teacher = Grade.objects.all().filter(subject_class__teacher=teacher, number=6).count()
    absences_in_school_count = Absence.objects.all().filter(student__school=school).count()
    absences_in_school_written_by_teacher_count = Absence.objects.all().filter(subject_class__teacher=teacher).count()
    remarks_in_school_count = Remark.objects.all().filter(student__school=school).count()
    remarks_in_school_written_by_teacher = Remark.objects.all().filter(teacher=teacher).count()
    praises_in_school_count = Praise.objects.all().filter(student__school=school).count()
    praises_in_school_written_by_teacher = Praise.objects.all().filter(teacher=teacher).count()

    context ={
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


@login_required(login_url='login')
def home(request):
    if request.user.is_staff:
        context = __get_context_for_admin_homepage__()
        return render(request, 'accounts/homepage_admin.html', context)

    if request.user.groups.filter(name='teacher').exists():
        teacher = Teacher.objects.get(user=request.user)
        context = __get_context_for_teacher_homepage__(teacher)
        return render(request, 'accounts/homepage_teacher.html', context)

    if request.user.groups.filter(name='student').exists():
        context = {}
        return render(request, 'accounts/homepage_student.html', context)

    if request.user.groups.filter(name='parent').exists():
        context = {}
        return render(request, 'accounts/homepage_parent.html', context)


@login_required(login_url='login')
@teacher_only
def students(request):
    teacher = Teacher.objects.get(user=request.user)
    teacher_school = teacher.school

    all_students_in_school = Student.objects.all().filter(
        school=teacher_school).order_by('class_level', 'student_number')

    context = {
        'school': teacher_school.name,
        'students': all_students_in_school,
    }
    return render(request, 'accounts/teacher/students.html', context)


@login_required(login_url='login')
@teacher_only
def teacher_subjects(request):
    teacher = Teacher.objects.get(user=request.user)

    all_subjects = Subject.objects.all().order_by('name')
    teacher_subject_classes = SubjectClass.objects.all().filter(
        teacher=teacher).order_by('subject__name', 'class_level')

    context = {
        'all_subjects': all_subjects,
        'teacher_subject_classes': teacher_subject_classes,
    }
    return render(request, 'accounts/teacher/teacher_subjects.html', context)


@login_required(login_url='login')
@teacher_only
def parents(request):
    teacher = Teacher.objects.get(user=request.user)
    teacher_school = teacher.school

    all_parents_in_school = Parent.objects.all().filter(
        school=teacher_school).order_by('first_name', 'last_name', 'child__first_name', 'child__last_name')

    context = {
        'school': teacher_school.name,
        'parents': all_parents_in_school,
    }
    return render(request, 'accounts/teacher/parents.html', context)


@login_required(login_url='login')
@teacher_only
def teacher_subject_class_detail(request, pk):
    teacher = Teacher.objects.get(user=request.user)

    subject_class = SubjectClass.objects.get(id=pk)
    subject_class_students = subject_class.students.all().order_by('student_number')
    all_grades = Grade.objects.all().filter(subject_class=subject_class)

    context = {
        'subject_class': subject_class,
        'subject_class_students': subject_class_students,
        'all_grades': all_grades,
    }
    return render(request, 'accounts/teacher/subject_class_detail.html', context)


@login_required(login_url='login')
@teacher_only
def teacher_absences(request):
    teacher = Teacher.objects.get(user=request.user)
    teacher_school = teacher.school
    all_subject_classes_of_teacher = SubjectClass.objects.all().filter(teacher=teacher)

    all_absences = []
    for subject_class in all_subject_classes_of_teacher:
        all_absences_for_subject_class = Absence.objects.all().filter(
            subject_class=subject_class)
        for absence in all_absences_for_subject_class:
            all_absences.append(absence)

    context = {
        'all_absences': all_absences,
        'school': teacher_school,
    }
    return render(request, 'accounts/teacher/teacher_absences.html', context)


@login_required(login_url='login')
@teacher_only
def teacher_remarks(request):
    teacher = Teacher.objects.get(user=request.user)
    all_remarks_made_by_teacher = Remark.objects.all().filter(
        teacher=teacher).order_by('term', 'student__first_name', 'student__last_name')

    context = {'remarks': all_remarks_made_by_teacher, 'teacher': teacher}
    return render(request, "accounts/teacher/teacher_remarks.html", context)


@login_required(login_url='login')
@teacher_only
def teacher_assign_student_to_parent(request, pk):
    teacher = Teacher.objects.get(user=request.user)
    teacher_school = teacher.school
    form = ParentTeacherUpdateForm()
    parent = Parent.objects.get(id=pk)

    all_students_from_school = Student.objects.all(
    ).filter(school=teacher_school)

    form.fields['child'] = forms.ModelChoiceField(
        queryset=all_students_from_school)

    if request.method == "POST":
        form = ParentTeacherUpdateForm(request.POST, instance=parent)
        if form.is_valid():
            form.save()
            return redirect("parents")
    context = {'form': form, 'parent': parent}
    return render(request, 'accounts/teacher/teacher_parent_update_form.html', context)


@login_required(login_url='login')
@teacher_only
def create_subject(request):
    form = SubjectCreateForm()

    if request.method == "POST":
        form = SubjectCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("teacher_subjects")
    context = {'form': form, }
    return render(request, 'accounts/teacher/subject_create_form.html', context)


@login_required(login_url='login')
@teacher_only
def create_subject_class(request):
    teacher = Teacher.objects.get(user=request.user)
    form = SubjectClassCreateForm()
    form.fields['teacher'] = forms.ModelChoiceField(
        queryset=Teacher.objects.all().filter(id=teacher.id))

    if request.method == "POST":
        form = SubjectClassCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("teacher_subjects")
    context = {'form': form, }
    return render(request, 'accounts/teacher/subject_class_create_form.html', context)


@login_required(login_url='login')
@teacher_only
def create_grade_for_student(request, pk):
    form = GradeForm()
    subject_class = SubjectClass.objects.get(id=pk)

    form.fields['student'] = forms.ModelChoiceField(
        queryset=subject_class.students)
    form.fields['subject_class'] = forms.ModelChoiceField(
        queryset=SubjectClass.objects.all().filter(id=pk))

    if request.method == "POST":
        form = GradeForm(request.POST, initial={
                         "subject_class": subject_class})
        if form.is_valid():
            form.save()
            return redirect("subject_class_detail", pk)
    context = {'form': form, }
    return render(request, 'accounts/teacher/grade_create_form.html', context)


@login_required(login_url='login')
@teacher_only
def create_absence(request, pk):
    form = AbsenceForm()
    subject_class = SubjectClass.objects.get(id=pk)
    students_for_subject_class = subject_class.students.all()
    form.fields['student'] = forms.ModelChoiceField(
        queryset=students_for_subject_class)
    form.fields['subject_class'] = forms.ModelChoiceField(
        queryset=SubjectClass.objects.all().filter(id=pk))

    if request.method == "POST":
        form = AbsenceForm(request.POST, initial={
                           "subject_class": subject_class})
        if form.is_valid():
            form.save()
            return redirect("subject_class_detail", pk)
    context = {'form': form, }
    return render(request, 'accounts/teacher/absence_create_form.html', context)


@login_required(login_url='login')
@teacher_only
def create_remark(request):
    form = RemarkForm()
    teacher = Teacher.objects.get(user=request.user)
    all_subject_classes = SubjectClass.objects.all().filter(teacher=teacher)
    students_pk_list = []
    for subject_class in all_subject_classes:
        for student in subject_class.students.all():
            students_pk_list.append(student.id)

    students = Student.objects.all().filter(pk__in=students_pk_list)

    form.fields['student'] = forms.ModelChoiceField(queryset=students)
    form.fields['teacher'] = forms.ModelChoiceField(
        queryset=Teacher.objects.all().filter(id=teacher.id))

    if request.method == "POST":
        form = RemarkForm(request.POST, initial={"students": students})
        if form.is_valid():
            form.save()
            return redirect("teacher_remarks")
    context = {'form': form, }
    return render(request, 'accounts/teacher/remark_create_form.html', context)


@login_required(login_url='login')
@teacher_only
def update_student(request, pk):
    student = Student.objects.get(id=pk)
    form = StudentUpdateForm(instance=student)
    if request.method == "POST":
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            user = student.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            form.save()
            return redirect("students")

    context = {'form': form}
    return render(request, 'accounts/teacher/student_update_form.html', context)


@login_required(login_url='login')
@teacher_only
def update_subject_class(request, pk):
    teacher = Teacher.objects.get(user=request.user)
    teacher_school = teacher.school

    subject_class = SubjectClass.objects.get(id=pk)
    form = SubjectClassUpdateForm(instance=subject_class)


    if request.method == "POST":
        form = SubjectClassUpdateForm(request.POST, instance=subject_class)
        if form.is_valid():
            form.save()
            return redirect("teacher_subjects")

    context = {'form': form}
    return render(request, 'accounts/teacher/subject_class_update_form.html', context)


@login_required(login_url='login')
@teacher_only
def update_grade(request, pk):
    grade = Grade.objects.get(id=pk)
    form = GradeUpdateForm(instance=grade)

    if request.method == "POST":
        form = GradeUpdateForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect("teacher_subjects")

    context = {'form': form, 'grade': grade}
    return render(request, 'accounts/teacher/grade_update_form.html', context)


@login_required(login_url='login')
@teacher_only
def update_absence(request, pk):
    absence = Absence.objects.get(id=pk)
    form = AbsenceForm(instance=absence)
    if request.method == "POST":
        form = AbsenceForm(request.POST, instance=absence)
        if form.is_valid():
            form.save()
            return redirect("teacher_absences")

    context = {'form': form, 'absence': absence}
    return render(request, 'accounts/teacher/absence_update_form.html', context)


@login_required(login_url='login')
@teacher_only
def update_remark(request, pk):
    teacher = Teacher.objects.get(user=request.user)
    remark = Remark.objects.get(id=pk)
    form = RemarkForm(instance=remark)

    form.fields['teacher'] = forms.ModelChoiceField(
        queryset=Teacher.objects.all().filter(id=teacher.id))

    if request.method == "POST":
        form = RemarkForm(request.POST, instance=remark)
        if form.is_valid():
            form.save()
            return redirect("teacher_remarks")
    context = {'form': form, 'remark': remark}
    return render(request, "accounts/teacher/remark_update_form.html", context)

@login_required(login_url='login')
@teacher_only
def edit_students_to_subject_class(request, pk):
    subject_class = SubjectClass.objects.get(id=pk)
    form = SubjectClassAddStudentsForm(instance=subject_class)

    teacher = Teacher.objects.get(user=request.user)
    teacher_school = teacher.school
    students = Student.objects.all().filter(school=teacher_school, class_level=subject_class.class_level)

    form.fields['students'] = forms.ModelMultipleChoiceField(queryset=students)
    if request.method == "POST":
        form = SubjectClassAddStudentsForm(request.POST, instance=subject_class)
        if form.is_valid():
            form.save()
            return redirect("subject_class_detail", pk)
    context = {'form': form, 'subject_class': subject_class, 'students': students}
    return render(request, "accounts/teacher/subject_class_edit_students_form.html", context)


@login_required(login_url='login')
@teacher_only
def remove_grade(request, pk):
    grade = Grade.objects.get(id=pk)
    if request.method == "POST":
        grade.delete()
        return redirect("teacher_subjects")

    context = {'item': grade}
    return render(request, 'accounts/teacher/delete_grade.html', context)


@login_required(login_url='login')
@teacher_only
def remove_absence(request, pk):
    absence = Absence.objects.get(id=pk)
    if request.method == "POST":
        absence.delete()
        return redirect("teacher_absences")
    context = {"item": absence}
    return render(request, "accounts/teacher/delete_absence.html", context)


@login_required(login_url='login')
@teacher_only
def remove_remark(request, pk):
    remark = Remark.objects.get(id=pk)
    if request.method == "POST":
        remark.delete()
        return redirect("teacher_remarks")
    context = {"item": remark}
    return render(request, "accounts/teacher/delete_remark.html", context)

@login_required(login_url='login')
@teacher_only
def remove_subject_class(request, pk):
    subject_class = SubjectClass.objects.get(id=pk)
    if request.method == "POST":
        subject_class.delete()
        return redirect("teacher_subjects")
    context = {"item": subject_class}
    return render(request, "accounts/teacher/delete_subject_class.html", context)
