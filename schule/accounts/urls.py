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

    path('teacher/assign-child-to-parent/<str:pk>/', views.teacher_assign_student_to_parent, name="add_child_to_parent"),
    path('teacher/create-subject/', views.create_subject, name="create_subject"),
    path('teacher/create-subject-class/', views.create_subject_class, name="create_subject_class"),
    path('teacher/create-grade/<str:pk>/', views.create_grade_for_student, name="create_grade"),

    path('teacher/update-student/<str:pk>/', views.update_student, name="update_student"),
    path('teacher/update-subject-class/<str:pk>/', views.update_subject_class, name="update_subject_class"),
    path('teacher/update-grade/<str:pk>/', views.update_grade, name="update_grade"),

    path('teacher/delete-grade/<str:pk>/', views.remove_grade, name="delete_grade"),

]