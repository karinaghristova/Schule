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
