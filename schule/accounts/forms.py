from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class CreateUserForm(UserCreationForm):
    CHOICES = (('parent', 'parent'), ('student', 'student'))
    all_schools = School.objects.all()
    SCHOOL_CHOICES = (tuple((s.name, f'{s.city.name}: {s.name}') for s in all_schools))
    role = forms.ChoiceField(choices=CHOICES)
    school_name = forms.ChoiceField(choices=SCHOOL_CHOICES)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class CreateUserFormTeacher(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = '__all__'

class GradeUpdateForm(ModelForm):
    class Meta:
        model = Grade
        fields = ['number']

class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'phone', 'class_level', 'student_number']

class ParentTeacherUpdateForm(ModelForm):
    class Meta:
        model = Parent
        fields = ['child']

class ParentUpdateForm(ModelForm):
    class Meta:
        model = Parent
        fields = ['first_name', 'last_name', 'phone', 'email']

class SubjectCreateForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

class SubjectClassCreateForm(ModelForm):
    class Meta:
        model = SubjectClass
        fields = ['class_level', 'subject', 'teacher']

class SubjectClassUpdateForm(ModelForm):
    class Meta:
        model = SubjectClass
        fields = ['class_level', 'subject', 'students']

class AbsenceForm(ModelForm):
    class Meta:
        model = Absence
        fields = '__all__'

class RemarkForm(ModelForm):
    class Meta:
        model = Remark
        fields = '__all__'

class PraiseForm(ModelForm):
    class Meta:
        model = Praise
        fields = '__all__'