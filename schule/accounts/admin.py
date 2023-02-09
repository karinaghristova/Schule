from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Absence)
admin.site.register(Remark)
admin.site.register(Praise)
admin.site.register(SubjectClass)
admin.site.register(Term)