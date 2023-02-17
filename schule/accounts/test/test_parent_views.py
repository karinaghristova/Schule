from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from accounts.models import *
import json

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
