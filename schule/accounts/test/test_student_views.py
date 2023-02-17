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
