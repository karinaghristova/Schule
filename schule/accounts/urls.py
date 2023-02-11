from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('register/teacher/', views.registerPageTeacher, name="registerTeacher"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    
    path('teacher/students/', views.teacher_students, name="students"),
    path('teacher/parents/', views.teacher_parents, name="parents"),
    path('teacher/subjects/', views.teacher_subjects, name="teacher_subjects"),
    path('teacher/subject_class/<str:pk>', views.teacher_subject_class_detail, name="subject_class_detail"),
    path('teacher/absences', views.teacher_absences, name="teacher_absences"),
    path('teacher/remarks', views.teacher_remarks, name="teacher_remarks"),
    path('teacher/praises', views.teacher_praises, name="teacher_praises"),

    path('teacher/assign-child-to-parent/<str:pk>/', views.teacher_assign_student_to_parent, name="add_child_to_parent"),
    path('teacher/create-subject/', views.teacher_create_subject, name="create_subject"),
    path('teacher/create-subject-class/', views.teacher_create_subject_class, name="create_subject_class"),
    path('teacher/create-grade/<str:pk>/', views.teacher_create_grade_for_student, name="create_grade"),
    path('teacher/create-absence/<str:pk>/', views.teacher_create_absence, name="add_absence"),
    path('teacher/create-remark', views.teacher_create_remark, name="create_remark"),
    path('teacher/create-praise', views.teacher_create_praise, name="create_praise"),

    path('teacher/update-student/<str:pk>/', views.teacher_update_student, name="update_student"),
    path('teacher/update-subject-class/<str:pk>/', views.teacher_update_subject_class, name="update_subject_class"),
    path('teacher/update-grade/<str:pk>/', views.teacher_update_grade, name="update_grade"),
    path('teacher/update-absence/<str:pk>/', views.teacher_update_absence, name="update_absence"),
    path('teacher/update-remark/<str:pk>/', views.teacher_update_remark, name="update_remark"),
    path('teacher/update-praise/<str:pk>/', views.teacher_update_praise, name="update_praise"),
    path('teacher/subject-class/add-students/<str:pk>', views.teacher_edit_students_to_subject_class, name="add_students_to_subject_class"),

    path('teacher/delete-grade/<str:pk>/', views.teacher_remove_grade, name="delete_grade"),
    path('teacher/delete-absence/<str:pk>/', views.teacher_remove_absence, name="delete_absence"),
    path('teacher/delete-remark/<str:pk>/', views.teacher_remove_remark, name="delete_remark"),
    path('teacher/delete-praise/<str:pk>/', views.teacher_remove_praise, name="delete_praise"),
    path('teacher/delete-subject-class/<str:pk>/', views.teacher_remove_subject_class, name="delete_subject_class"),

    path('parent/account', views.parent_account, name="parent_account"),
    path('parent/grades', views.parent_grades, name="parent_grades"),
    path('parent/absences', views.parent_absences, name="parent_absences"),
    path('parent/remarks', views.parent_remarks, name="parent_remarks"),
    path('parent/praises', views.parent_praises, name="parent_praises"),

    path('parent/update-info', views.parent_update_info, name="parent_update_info"),

    path('student/account', views.student_account, name="student_account"),
    path('student/grades', views.student_grades, name="student_grades"),
    path('student/absences', views.student_absences, name="student_absences"),
    path('student/remarks', views.student_remarks, name="student_remarks"),
    path('student/praises', views.student_praises, name="student_praises"),

    path('student/update-info', views.student_update_info, name="student_update_info"),

]