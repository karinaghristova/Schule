from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('register/teacher/', views.registerPageTeacher, name="registerTeacher"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    
    path('teacher/students/', views.students, name="students"),
    path('teacher/parents/', views.parents, name="parents"),
    path('teacher/subjects/', views.teacher_subjects, name="teacher_subjects"),
    path('teacher/subject_class/<str:pk>', views.teacher_subject_class_detail, name="subject_class_detail"),
    path('teacher/absences', views.teacher_absences, name="teacher_absences"),
    path('teacher/remarks', views.teacher_remarks, name="teacher_remarks"),
    path('teacher/praises', views.teacher_praises, name="teacher_praises"),

    path('teacher/assign-child-to-parent/<str:pk>/', views.teacher_assign_student_to_parent, name="add_child_to_parent"),
    path('teacher/create-subject/', views.create_subject, name="create_subject"),
    path('teacher/create-subject-class/', views.create_subject_class, name="create_subject_class"),
    path('teacher/create-grade/<str:pk>/', views.create_grade_for_student, name="create_grade"),
    path('teacher/create-absence/<str:pk>/', views.create_absence, name="add_absence"),
    path('teacher/create-remark', views.create_remark, name="create_remark"),
    path('teacher/create-praise', views.create_praise, name="create_praise"),

    path('teacher/update-student/<str:pk>/', views.update_student, name="update_student"),
    path('teacher/update-subject-class/<str:pk>/', views.update_subject_class, name="update_subject_class"),
    path('teacher/update-grade/<str:pk>/', views.update_grade, name="update_grade"),
    path('teacher/update-absence/<str:pk>/', views.update_absence, name="update_absence"),
    path('teacher/update-remark/<str:pk>/', views.update_remark, name="update_remark"),
    path('teacher/update-praise/<str:pk>/', views.update_praise, name="update_praise"),
    path('teacher/subject-class/add-students/<str:pk>', views.edit_students_to_subject_class, name="add_students_to_subject_class"),

    path('teacher/delete-grade/<str:pk>/', views.remove_grade, name="delete_grade"),
    path('teacher/delete-absence/<str:pk>/', views.remove_absence, name="delete_absence"),
    path('teacher/delete-remark/<str:pk>/', views.remove_remark, name="delete_remark"),
    path('teacher/delete-praise/<str:pk>/', views.remove_praise, name="delete_praise"),
    path('teacher/delete-subject-class/<str:pk>/', views.remove_subject_class, name="delete_subject_class"),

]