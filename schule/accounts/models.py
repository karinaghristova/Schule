from django.db import models
from django.contrib.auth.models import User

from datetime import date

# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(
        User, null=False, blank=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=False)
    last_name = models.CharField(max_length=200, blank=False)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True, blank=False)

    def __str__(self):
        return f'Mr/Mrs {self.first_name} {self.last_name}'

class Student(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=False)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, blank=False)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True, blank=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Parent(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=False)
    last_name = models.CharField(max_length=200, blank=False)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True, blank=False)
    child = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Subject(models.Model):
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.name

class Term(models.Model):
    CHOICES = (('winter', 'winter'), ('summer', 'summer'))
    name = models.CharField(max_length=20, null=True, blank=False, choices=CHOICES)

    def __str__(self):
        return self.name


class Grade(models.Model):
    number = models.DecimalField(max_digits=3, decimal_places=2, blank=False)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE, blank=False)
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE, blank=False)
    term = models.ForeignKey(Term, null=True, blank=False, on_delete=models.SET_NULL)

    def __str__(self):
        return self.number


class Absence(models.Model):
    date = models.DateField(default=date.today, blank=False)
    excused = models.BooleanField(default=False, blank=False)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.CASCADE, blank=False)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE, blank=False)
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE, blank=False)
    term = models.ForeignKey(Term, null=True, blank=False, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.student.first_name} was absent on {self.date} in {self.subject.name} class'


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


class SubjectClass(models.Model):
    subject = models.ForeignKey(Subject, null=True, on_delete=models.CASCADE, blank=False)
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE, blank=False)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return f'{self.subject} class of Mr/Mrs {self.teacher.last_name}'


