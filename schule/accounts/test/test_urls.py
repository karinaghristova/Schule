from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import *


class TestAuthUrls(SimpleTestCase):
    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, registerPage)

    def test_register_teacher_url_is_resolved(self):
        url = reverse('registerTeacher')
        self.assertEquals(resolve(url).func, registerPageTeacher)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, loginPage)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logoutUser)


