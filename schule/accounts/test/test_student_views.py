from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from accounts.models import *
import json


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

class TestStudentViewsAccessibility(TestCase):
    def setUp(self):
        self.client = Client()

        self.city = City.objects.create(name='City')
        self.school = School.objects.create(name='TestSchool', city=self.city)

        self.groupless_user = User.objects.create_user(
            username='testuser', password='password',
            first_name='TestUser', last_name='TestUser',
            email='testuser@email.com')

        self.teacher_user = User.objects.create_user(
            username='teacher', password='password',
            first_name='Teacher', last_name='Teacher',
            email='teacher@email.com')
        self.teacher = Teacher.objects.create(user=self.teacher_user,
        first_name=self.teacher_user.first_name, last_name=self.teacher_user.last_name,
        email=self.teacher_user.email, school=self.school)

        self.student_user = User.objects.create_user(
        username='student', password='password',
        first_name='Student', last_name='Student', email='student@email.com')
        self.student = Student.objects.create(user=self.student_user,
        first_name=self.student_user.first_name, last_name=self.student_user.last_name, 
        email=self.student_user.email, school=self.school,
        class_level=10, student_number=1)

        self.parent_user = User.objects.create_user(
        username='parent', password='password',
        first_name='Parent', last_name='Parent', email='parent@email.com')
        self.parent = Parent.objects.create(user=self.parent_user,
        first_name=self.parent_user.first_name, last_name=self.parent_user.last_name,
        email=self.parent_user.email, school=self.school, child=self.student)

        self.teacher_group = Group.objects.create(name='teacher')
        self.parent_group = Group.objects.create(name='parent')
        self.student_group = Group.objects.create(name='student')

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


    def test_student_account_view_is_accessible_for_users_with_group_student_only(self):
        self.client.login(username='student', password='password')
        response = self.client.get(reverse('student_account'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/student/student_account.html')

        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('student_account'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('student_account'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('student_account'))

        self.assertEqual(response.status_code, 302)

    def test_student_grades_view_is_accessible_for_users_with_group_student_only(self):
        self.client.login(username='student', password='password')
        response = self.client.get(reverse('student_grades'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/grades_account.html')

        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('student_grades'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('student_grades'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('student_grades'))

        self.assertEqual(response.status_code, 302)

    def test_student_absences_view_is_accessible_for_users_with_group_student_only(self):
        self.client.login(username='student', password='password')
        response = self.client.get(reverse('student_absences'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/absences.html')

        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('student_absences'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('student_absences'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('student_absences'))

        self.assertEqual(response.status_code, 302)

    def test_student_remarks_view_is_accessible_for_users_with_group_student_only(self):
        self.client.login(username='student', password='password')
        response = self.client.get(reverse('student_remarks'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/remarks.html')

        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('student_remarks'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('student_remarks'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('student_remarks'))

        self.assertEqual(response.status_code, 302)

    def test_student_praises_view_is_accessible_for_users_with_group_student_only(self):
        self.client.login(username='student', password='password')
        response = self.client.get(reverse('student_praises'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/praises.html')

        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('student_praises'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('student_praises'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('student_praises'))

        self.assertEqual(response.status_code, 302)
