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

        self.teacher = User.objects.create_user(
            username='teacher', password='password')
        self.parent = User.objects.create_user(
            username='parent', password='password')
        self.student = User.objects.create_user(
            username='student', password='password')
        self.admin = User.objects.create_user(
            username='admin', password='password')

        self.admin_group = Group.objects.create(name='admin')
        self.teacher_group = Group.objects.create(name='teacher')
        self.parent_group = Group.objects.create(name='parent')
        self.student_group = Group.objects.create(name='student')

        self.admin.groups.add(self.admin_group)
        self.teacher.groups.add(self.teacher_group)
        self.parent.groups.add(self.parent_group)
        self.student.groups.add(self.student_group)

    def tes_home_view_is_accessible_for_users_with_group_admin(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/homepage_admin.html')

    def tes_home_view_is_accessible_for_users_with_group_teacher(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/homepage_teacher.html')

    def tes_home_view_is_accessible_for_users_with_group_parent(self):
        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/homepage_parent.html')

    def tes_home_view_is_accessible_for_users_with_group_student(self):
        self.client.login(username='student', password='password')
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/homepage_student.html')


class TestTeacherViewsWithRequiredLogin(TestCase):
    def test_teacher_account_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('teacher_account'))

        self.assertEquals(response.status_code, 302)

    def test_teacher_students_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('students'))

        self.assertEquals(response.status_code, 302)

    def test_teacher_parents_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('parents'))

        self.assertEquals(response.status_code, 302)

    def test_teacher_subjects_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('teacher_subjects'))

        self.assertEquals(response.status_code, 302)

    def test_teacher_subject_class_detail_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(
            reverse('subject_class_detail', args=['some_pk']))

        self.assertEquals(response.status_code, 302)

    def test_teacher_absences_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('teacher_absences'))

        self.assertEquals(response.status_code, 302)

    def test_teacher_remarks_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('teacher_remarks'))

        self.assertEquals(response.status_code, 302)

    def test_teacher_praises_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('teacher_praises'))

        self.assertEquals(response.status_code, 302)


class TestParentViewsWithRequiredLogin(TestCase):
    def test_parent_account_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('parent_account'))

        self.assertEquals(response.status_code, 302)

    def test_parent_grades_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('parent_grades'))

        self.assertEquals(response.status_code, 302)

    def test_parent_absences_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('parent_absences'))

        self.assertEquals(response.status_code, 302)

    def test_parent_remarks_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('parent_remarks'))

        self.assertEquals(response.status_code, 302)

    def test_parent_praises_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('parent_praises'))

        self.assertEquals(response.status_code, 302)

    def test_parent_update_info_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('parent_update_info'))

        self.assertEquals(response.status_code, 302)


class TestStudentViewsWithRequiredLogin(TestCase):
    def test_student_account_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('student_account'))

        self.assertEquals(response.status_code, 302)

    def test_student_grades_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('student_grades'))

        self.assertEquals(response.status_code, 302)

    def test_student_absences_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('student_absences'))

        self.assertEquals(response.status_code, 302)

    def test_student_remarks_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('student_remarks'))

        self.assertEquals(response.status_code, 302)

    def test_student_praises_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('student_praises'))

        self.assertEquals(response.status_code, 302)

    def test_student_update_info_view_redirects_for_unathenticated_users_GET(self):
        response = self.client.get(reverse('student_update_info'))

        self.assertEquals(response.status_code, 302)
