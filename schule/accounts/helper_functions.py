from accounts.models import *

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
            average_grade_winter =  sum(value['grades_winter']) / len(value['grades_winter'])
            value['average_grade_winter'] = "{:.2f}".format(average_grade_winter)
        if len(value['grades_summer']) > 0:
            average_grade_summer =  sum(value['grades_summer']) / len(value['grades_summer'])
            value['average_grade_summer'] = "{:.2f}".format(average_grade_summer)
    
    return student_grades

def get_student_absences(student):
    absences = Absence.objects.all().filter(student=student).order_by('date')
    return absences

def get_student_remarks(student):
    remarks = Remark.objects.all().filter(student=student)
    return remarks

def get_student_praises(student):
    praises = Praise.objects.all().filter(student=student)
    return praises