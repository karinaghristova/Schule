from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from accounts.models import *
import json


class TestAuthViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_page_GET(self):
        response = self.client.get(reverse('register'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('accounts/register.html')

    def test_register_page_teacher_GET(self):
        response = self.client.get(reverse('register'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('accounts/register.html')

    def test_login_GET(self):
        response = self.client.get(reverse('login'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('accounts/login.html')


class TestHomeViewWithRequiredLogin(TestCase):
    def test_home_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('home'))

        self.assertEquals(response.status_code, 302)


class TestHomeView(TestCase):
    def setUp(self):
        self.client = Client()

        self.city = City.objects.create(name='City')
        self.school = School.objects.create(name='TestSchool', city=self.city)

        self.teacher_user = User.objects.create_user(
            username='teacher', password='password', 
            first_name='Teacher', last_name='Teacher', 
            email='teacher@email.com')
        self.teacher = Teacher.objects.create(user=self.teacher_user,
        first_name=self.teacher_user.first_name, last_name=self.teacher_user.last_name, 
        email=self.teacher_user.email, school=self.school)
        
        self.student_user = User.objects.create_user(
            username='student', password='password',
            first_name='Student', last_name='Student', 
            email='student@email.com')
        self.student = Student.objects.create(user=self.student_user,
        first_name=self.student_user.first_name, last_name=self.student_user.last_name, 
        email=self.student_user.email, school=self.school,
        class_level=10, student_number=1)

        self.parent_user = User.objects.create_user(
            username='parent', password='password',
            first_name='Parent', last_name='Parent', email='parent@email.com')
        self.parent = Parent.objects.create(user=self.parent_user,
        first_name=self.parent_user.first_name, last_name=self.parent_user.last_name, 
        email=self.parent_user.email, school=self.school)

        self.admin_user = User.objects.create_superuser(
            username='admin', password='password',
            first_name='Admin', last_name='Admin', email='admin@email.com')

        self.admin_group = Group.objects.create(name='admin')
        self.teacher_group = Group.objects.create(name='teacher')
        self.parent_group = Group.objects.create(name='parent')
        self.student_group = Group.objects.create(name='student')

        self.admin_user.groups.add(self.admin_group)
        self.teacher_user.groups.add(self.teacher_group)
        self.parent_user.groups.add(self.parent_group)
        self.student_user.groups.add(self.student_group)

        self.subject = Subject.objects.create(name='Subject')
        self.subject_class = SubjectClass.objects.create(class_level=10, 
        subject=self.subject, teacher=self.teacher)
        self.subject_class.students.add(self.student)

        self.winter_term = Term.objects.create(name='winter')
        self.summer_term = Term.objects.create(name='summer')

        self.winter_grade = Grade.objects.create(number=4, 
        student=self.student, subject_class=self.subject_class, 
        term=self.winter_term)

        self.summer_grade = Grade.objects.create(number=4, 
        student=self.student, subject_class=self.subject_class, 
        term=self.summer_term)


    def test_home_view_is_accessible_for_staff_users(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/homepage_admin.html')

    def test_home_view_is_accessible_for_users_with_group_teacher(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/homepage_teacher.html')

    def test_home_view_is_accessible_for_users_with_group_parent(self):
        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/homepage_parent.html')

    def test_home_view_is_accessible_for_users_with_group_student(self):
        self.client.login(username='student', password='password')
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/homepage_student.html')
