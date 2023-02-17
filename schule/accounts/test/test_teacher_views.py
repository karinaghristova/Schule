from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from accounts.models import *
import json

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

