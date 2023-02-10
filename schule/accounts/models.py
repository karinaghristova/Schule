from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from datetime import date


class City(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=True)
    
    def __str__(self):
        return self.name

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=200, blank=False)
    city = models.ForeignKey(City, blank=False, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(
        User, null=False, blank=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, default="No name", blank=False)
    last_name = models.CharField(max_length=200, default="No name", blank=False)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True, blank=False)
    school = models.ForeignKey(School, blank=False, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'Mr/Mrs {self.first_name} {self.last_name}'

class Student(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, default="No name", blank=False)
    middle_name = models.CharField(max_length=200, default="No name", null=True, blank=True)
    last_name = models.CharField(max_length=200, default="No name", blank=False)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True, blank=False)
    grade_average = models.DecimalField(max_digits=3, default=2.00, decimal_places=2, blank=False)
    school = models.ForeignKey(School, blank=False, null=True, on_delete=models.SET_NULL)
    class_level = models.IntegerField(blank=False, default=1, validators=[MinValueValidator(1), MaxValueValidator(12)])
    student_number = models.IntegerField(blank=False, default=1, validators=[MinValueValidator(1), MaxValueValidator(30)])

    def __str__(self):
        return f'{self.student_number}: {self.first_name} {self.last_name}'

class Parent(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, default="No name", blank=False)
    last_name = models.CharField(max_length=200, default="No name", blank=False)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True, blank=False)
    child = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    school = models.ForeignKey(School, blank=False, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Subject(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=True)

    def __str__(self):
        return self.name

class SubjectClass(models.Model):
    class_level = models.IntegerField(blank=False, default=1, validators=[MinValueValidator(1), MaxValueValidator(12)])
    subject = models.ForeignKey(Subject, null=True, on_delete=models.CASCADE, blank=False)
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE, blank=False)
    students = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return f'{self.subject} class of Mr/Mrs {self.teacher.last_name}'

class Term(models.Model):
    CHOICES = (('winter', 'winter'), ('summer', 'summer'))
    name = models.CharField(max_length=20, null=True, blank=False, choices=CHOICES)

    def __str__(self):
        return self.name


class Grade(models.Model):
    CHOICES = ((2, 'Failure 2'), (3, 'Passing 3'), (4, 'Good 4'), (5, 'Very good 5'), (6, 'Excellent 6'))
    number = models.IntegerField(blank=False, choices=CHOICES)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE, blank=False)
    subject_class = models.ForeignKey(SubjectClass, null=True, on_delete=models.CASCADE, blank=False)
    term = models.ForeignKey(Term, null=True, blank=False, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.number}'


class Absence(models.Model):
    date = models.DateField(default=date.today, blank=False)
    excused = models.BooleanField(default=False, blank=False)
    subject_class = models.ForeignKey(SubjectClass, null=True, on_delete=models.CASCADE, blank=False)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE, blank=False)
    term = models.ForeignKey(Term, null=True, blank=False, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.student.first_name} was absent on {self.date}'


class Remark(models.Model):
    content = models.CharField(max_length=500, blank=False)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE, blank=False)
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE, blank=False)
    term = models.ForeignKey(Term, null=True, blank=False, on_delete=models.SET_NULL)

    def __str__(self):
        return self.content


class Praise(models.Model):
    content = models.CharField(max_length=500, blank=False)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE, blank=False)
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE, blank=False)
    term = models.ForeignKey(Term, null=True, blank=False, on_delete=models.SET_NULL)

    def __str__(self):
        return self.content





