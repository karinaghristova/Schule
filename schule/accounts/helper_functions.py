from django.db.models import Avg
from accounts.models import *


def get_average_grade_of_student(student):
    average_grade = Grade.objects.all().filter(student=student).aggregate(Avg('number'))
    avg = "{:.2f}".format(average_grade['number__avg'])
    return avg

def get_average_grade_for_subject_in_term_of_student(student, subject, term):
    average_grade = Grade.objects.all().filter(
        student=student, subject_class__subject__name=subject, term__name=term).aggregate(Avg('number'))
    avg = "{:.2f}".format(average_grade['number__avg'])
    return avg

def get_average_grade_for_term_of_student(student, term):
    average_grade = Grade.objects.all().filter(
        student=student, term__name=term).aggregate(Avg('number'))
    avg = "{:.2f}".format(average_grade['number__avg'])
    return avg

def get_count_of_grades_by_value(student, value):
    grades = Grade.objects.all().filter(student=student, number=value).count()
    return grades

def get_count_of_grades_by_value_and_term(student, value, term):
    grades = Grade.objects.all().filter(student=student, number=value, term__name=term).count()
    return grades

def get_count_of_grades_by_term(student, term):
    grades = Grade.objects.all().filter(student=student, term__name=term).count()
    return grades


def get_count_of_grades_for_student(student):
    grades_count = Grade.objects.all().filter(student=student).count()
    return grades_count

def get_student_grades(student):
    grades = Grade.objects.all().filter(student=student).order_by('subject_class__subject__name')

    student_grades = {}
    for grade in grades:
        grade_value = grade.number
        subject = grade.subject_class.subject.name
        
        if subject not in student_grades:
            student_grades[subject] = {'grades_winter': [], 'average_grade_winter': 2.0,
            'grades_summer': [], 'average_grade_summer': 2.0}

        if grade.term.name == 'winter':
            student_grades[subject]['grades_winter'].append(grade_value)
        else:
            student_grades[subject]['grades_summer'].append(grade_value)
    
    for subject, value in student_grades.items():
        if len(value['grades_winter']) > 0:
            value['average_grade_winter'] =  get_average_grade_for_subject_in_term_of_student(student, subject, 'winter')
        if len(value['grades_summer']) > 0:
            value['average_grade_summer'] = get_average_grade_for_subject_in_term_of_student(student, subject, 'summer')
    
    return student_grades

def get_student_absences(student):
    absences = Absence.objects.all().filter(student=student).order_by('date')
    return absences

def get_count_of_student_absences(student):
    absences_count = Absence.objects.all().filter(student=student).count()
    return absences_count

def get_student_absences_for_term(student, term):
    absences = Absence.objects.all().filter(student=student, term__name=term).order_by('date')
    return absences

def get_count_of_student_absences_for_term(student, term):
    absences_count = Absence.objects.all().filter(student=student, term__name=term).count()
    return absences_count

def get_student_remarks(student):
    remarks = Remark.objects.all().filter(student=student)
    return remarks

def get_count_of_student_remarks(student):
    remarks_count = Remark.objects.all().filter(student=student).count()
    return remarks_count

def get_student_remarks_for_term(student, term):
    remarks = Remark.objects.all().filter(student=student, term__name=term)
    return remarks

def get_count_of_student_remarks_for_term(student, term):
    remarks_count = Remark.objects.all().filter(student=student, term__name=term).count()
    return remarks_count

def get_student_praises(student):
    praises = Praise.objects.all().filter(student=student)
    return praises

def get_count_of_student_praises(student):
    praises_count = Praise.objects.all().filter(student=student).count()
    return praises_count

def get_count_of_student_praises_for_term(student, term):
    praises = Praise.objects.all().filter(student=student, term__name=term)
    return praises

def get_count_of_student_praises_for_term(student, term):
    praises_count = Praise.objects.all().filter(student=student, term__name=term).count()
    return praises_count
