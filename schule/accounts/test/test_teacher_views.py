from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from accounts.models import *
import json

from datetime import date


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


class TestTeacherViewsAccessibility(TestCase):
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

        self.absence = Absence.objects.create(date=date.today(),
                                              excused=False, subject_class=self.subject_class,
                                              student=self.student, term=self.winter_term)

        self.remark = Remark.objects.create(content='This is a remark',
                                            student=self.student, teacher=self.teacher, term=self.winter_term)

        self.praise = Praise.objects.create(content='This is a praise',
                                            student=self.student, teacher=self.teacher, term=self.winter_term)

    def test_teacher_account_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('teacher_account'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/teacher_account.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('teacher_account'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(reverse('teacher_account'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('teacher_account'))

        self.assertEqual(response.status_code, 302)

    def test_teacher_update_info_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('teacher_update_info'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/account_update_form.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('teacher_update_info'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(reverse('teacher_update_info'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('teacher_update_info'))

        self.assertEqual(response.status_code, 302)

    def test_teacher_students_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('students'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/students.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('students'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(reverse('students'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('students'))

        self.assertEqual(response.status_code, 302)

    def test_teacher_subjects_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('teacher_account'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/teacher_subjects.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('teacher_subjects'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(reverse('teacher_subjects'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('teacher_subjects'))

        self.assertEqual(response.status_code, 302)

    def test_teacher_parents_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('parents'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/parents.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('parents'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(reverse('parents'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('parents'))

        self.assertEqual(response.status_code, 302)

    def test_teacher_subject_class_detail_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(
            reverse('subject_class_detail', args=[self.subject_class.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/subject_class_detail.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(
            reverse('subject_class_detail', args=[self.subject_class.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(
            reverse('subject_class_detail', args=[self.subject_class.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('subject_class_detail', args=[self.subject_class.id]))

        self.assertEqual(response.status_code, 302)

    def test_teacher_absences_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('teacher_absences'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/teacher_absences.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('teacher_absences'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(reverse('teacher_absences'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('teacher_absences'))

        self.assertEqual(response.status_code, 302)

    def test_teacher_remarks_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('teacher_remarks'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/teacher_remarks.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('teacher_remarks'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(reverse('teacher_remarks'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('teacher_remarks'))

        self.assertEqual(response.status_code, 302)

    def test_teacher_praises_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('teacher_praises'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/teacher_praises.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('teacher_praises'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(reverse('teacher_praises'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('teacher_praises'))

        self.assertEqual(response.status_code, 302)

    def test_teacher_assign_student_to_parent_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(
            reverse('add_child_to_parent', args=[self.parent.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            'accounts/teacher/teacher_parent_update_form.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(
            reverse('add_child_to_parent', args=[self.parent.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(
            reverse('add_child_to_parent', args=[self.parent.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('add_child_to_parent', args=[self.parent.id]))

        self.assertEqual(response.status_code, 302)

    def test_teacher_create_subject_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('create_subject'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/subject_create_form.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('create_subject'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(reverse('create_subject'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('create_subject'))

        self.assertEqual(response.status_code, 302)

    def test_teacher_create_subject_class_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('create_subject_class'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            'accounts/teacher/subject_class_create_form.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('create_subject_class'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(reverse('create_subject_class'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('create_subject_class'))

        self.assertEqual(response.status_code, 302)

    def test_teacher_create_grade_for_student_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(
            reverse('create_grade', args=[self.student.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/grade_create_form.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(
            reverse('create_grade', args=[self.student.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(
            reverse('create_grade', args=[self.student.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('create_grade', args=[self.student.id]))

        self.assertEqual(response.status_code, 302)

    def test_teacher_create_absence_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(
            reverse('add_absence', args=[self.student.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/absence_create_form.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(
            reverse('add_absence', args=[self.student.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(
            reverse('add_absence', args=[self.student.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('add_absence', args=[self.student.id]))

        self.assertEqual(response.status_code, 302)

    def test_teacher_create_remark_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('create_remark'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/remark_create_form.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('create_remark'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(reverse('create_remark'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('create_remark'))

        self.assertEqual(response.status_code, 302)

    def test_teacher_create_praise_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(reverse('create_praise'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/praise_create_form.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('create_praise'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(reverse('create_praise'))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('create_praise'))

        self.assertEqual(response.status_code, 302)

    def test_teacher_update_student_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(
            reverse('update_student', args=[self.student.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/student_update_form.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(
            reverse('update_student', args=[self.student.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(
            reverse('update_student', args=[self.student.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('update_student', args=[self.student.id]))

        self.assertEqual(response.status_code, 302)

    def test_teacher_update_subject_class_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(
            reverse('update_subject_class', args=[self.subject_class.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            'accounts/teacher/subject_class_update_form.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(
            reverse('update_subject_class', args=[self.subject_class.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(
            reverse('update_subject_class', args=[self.subject_class.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('update_subject_class', args=[self.subject_class.id]))

        self.assertEqual(response.status_code, 302)

    def test_teacher_update_grade_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(
            reverse('update_grade', args=[self.winter_grade.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/grade_update_form.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(
            reverse('update_grade', args=[self.winter_grade.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(
            reverse('update_grade', args=[self.winter_grade.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('update_grade', args=[self.winter_grade.id]))

        self.assertEqual(response.status_code, 302)

    def test_teacher_update_absence_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(
            reverse('update_absence', args=[self.absence.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/absence_update_form.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(
            reverse('update_absence', args=[self.absence.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(
            reverse('update_absence', args=[self.absence.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('update_absence', args=[self.absence.id]))

        self.assertEqual(response.status_code, 302)

    def test_teacher_update_remark_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(
            reverse('update_remark', args=[self.remark.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/remark_update_form.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(
            reverse('update_remark', args=[self.remark.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(
            reverse('update_remark', args=[self.remark.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('update_remark', args=[self.remark.id]))

        self.assertEqual(response.status_code, 302)

    def test_teacher_update_praise_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(
            reverse('update_praise', args=[self.praise.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/praise_update_form.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(
            reverse('update_praise', args=[self.praise.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(
            reverse('update_praise', args=[self.praise.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('update_praise', args=[self.praise.id]))

        self.assertEqual(response.status_code, 302)

    def test_teacher_remove_absence_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(
            reverse('delete_absence', args=[self.absence.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/delete_absence.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(
            reverse('delete_absence', args=[self.absence.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(
            reverse('delete_absence', args=[self.absence.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('delete_absence', args=[self.absence.id]))

        self.assertEqual(response.status_code, 302)

    def test_teacher_remove_grade_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(
            reverse('delete_grade', args=[self.winter_grade.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/delete_grade.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(
            reverse('delete_grade', args=[self.winter_grade.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(
            reverse('delete_grade', args=[self.winter_grade.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('delete_grade', args=[self.winter_grade.id]))

        self.assertEqual(response.status_code, 302)

    def test_teacher_remove_remark_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(
            reverse('delete_remark', args=[self.remark.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/delete_remark.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(
            reverse('delete_remark', args=[self.remark.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(
            reverse('delete_remark', args=[self.remark.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('delete_remark', args=[self.remark.id]))

        self.assertEqual(response.status_code, 302)

    def test_teacher_remove_praise_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(
            reverse('delete_praise', args=[self.praise.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/delete_praise.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(
            reverse('delete_praise', args=[self.praise.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(
            reverse('delete_praise', args=[self.praise.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('delete_praise', args=[self.praise.id]))

        self.assertEqual(response.status_code, 302)

    def test_teacher_remove_subject_class_view_GET_is_accessible_for_users_with_group_teacher_only(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(
            reverse('delete_subject_class', args=[self.subject_class.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/teacher/delete_subject_class.html')

        self.client.login(username='parent', password='password')
        response = self.client.get(
            reverse('delete_subject_class', args=[self.subject_class.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='student', password='password')
        response = self.client.get(
            reverse('delete_subject_class', args=[self.subject_class.id]))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('delete_subject_class', args=[self.subject_class.id]))

        self.assertEqual(response.status_code, 302)


class TeacherViewsWithPOST(TestCase):
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
                                            email=self.parent_user.email, school=self.school)

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

    def test_teacher_create_subject_POST_adds_subject(self):
        self.client.login(username='teacher', password='password')
        url = reverse('create_subject')

        data = {'name': 'Subject2'}

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Subject.objects.all()[1].name, 'Subject2')

    def test_teacher_create_subject_POST_no_data_does_not_add_subject(self):
        self.client.login(username='teacher', password='password')
        url = reverse('create_subject')

        data = {}

        response = self.client.post(url, data)

        self.assertEquals(Subject.objects.count(), 1)
        self.assertEquals(response.status_code, 200)

    def test_teacher_create_subject_class_POST_adds_subject_class(self):
        self.client.login(username='teacher', password='password')
        url = reverse('create_subject_class')

        class_level = 1
        data = {
            'class_level': class_level,
            'subject': self.subject.id,
            'teacher': self.teacher.id,
        }

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(SubjectClass.objects.all()[
                          1].class_level, class_level)
        self.assertEquals(SubjectClass.objects.all()[1].subject, self.subject)
        self.assertEquals(SubjectClass.objects.all()[1].teacher, self.teacher)

    def test_teacher_create_subject_class_POST_no_data_does_not_add_subject_class(self):
        self.client.login(username='teacher', password='password')
        url = reverse('create_subject_class')

        data = {}

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 200)

    def test_teacher_teacher_create_absence_POST_adds_absence(self):
        self.client.login(username='teacher', password='password')
        url = reverse('add_absence', args=[self.subject_class.id])

        date_today = date.today()
        data = {
            'date': date_today,
            'excused': True,
            'subject_class': self.subject_class.id,
            'student': self.student.id,
            'term': self.winter_term.id,
        }

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Absence.objects.count(), 1)
        self.assertEquals(Absence.objects.first().date, date_today)
        self.assertEquals(Absence.objects.first().excused, True)
        self.assertEquals(
            Absence.objects.first().subject_class, self.subject_class)
        self.assertEquals(Absence.objects.first().student, self.student)
        self.assertEquals(Absence.objects.first().term, self.winter_term)

    def test_teacher_create_absence_POST_no_data_does_not_add_absence(self):
        self.client.login(username='teacher', password='password')
        url = reverse('add_absence', args=[self.subject_class.id])

        data = {}

        response = self.client.post(url, data)

        self.assertEquals(Absence.objects.count(), 0)
        self.assertEquals(response.status_code, 200)

    def test_teacher_create_remark_POST_adds_remark(self):
        self.client.login(username='teacher', password='password')
        url = reverse('create_remark')

        content = 'Some content'
        data = {
            'content': content,
            'student': self.student.id,
            'teacher': self.teacher.id,
            'term': self.winter_term.id,
        }

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Remark.objects.count(), 1)
        self.assertEquals(Remark.objects.first().content, content)
        self.assertEquals(Remark.objects.first().student, self.student)
        self.assertEquals(Remark.objects.first().teacher, self.teacher)
        self.assertEquals(Remark.objects.first().term, self.winter_term)

    def test_teacher_create_remark_POST_no_data_does_not_add_remark(self):
        self.client.login(username='teacher', password='password')
        url = reverse('create_remark')

        data = {}

        response = self.client.post(url, data)

        self.assertEquals(Remark.objects.count(), 0)
        self.assertEquals(response.status_code, 200)

    def test_teacher_create_praise_POST_adds_praise(self):
        self.client.login(username='teacher', password='password')
        url = reverse('create_praise')

        content = 'Some content'
        data = {
            'content': content,
            'student': self.student.id,
            'teacher': self.teacher.id,
            'term': self.winter_term.id,
        }

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Praise.objects.count(), 1)
        self.assertEquals(Praise.objects.first().content, content)
        self.assertEquals(Praise.objects.first().student, self.student)
        self.assertEquals(Praise.objects.first().teacher, self.teacher)
        self.assertEquals(Praise.objects.first().term, self.winter_term)

    def test_teacher_create_praise_POST_no_data_does_not_add_praise(self):
        self.client.login(username='teacher', password='password')
        url = reverse('create_praise')

        data = {}

        response = self.client.post(url, data)

        self.assertEquals(Praise.objects.count(), 0)
        self.assertEquals(response.status_code, 200)

    def test_teacher_update_student_POST_updates_student(self):
        self.client.login(username='teacher', password='password')
        url = reverse('update_student', args=[self.student.id])

        student_first_name = 'Ivan'
        student_middle_name = 'Ivanov'
        student_last_name = 'Ivanov'
        student_phone = '+359624865795396'
        student_email = self.student.email
        student_school = self.student.school
        student_class_level = 10
        student_student_number = self.student.student_number

        data = {
            'first_name': student_first_name,
            'middle_name': student_middle_name,
            'last_name': student_last_name,
            'email': student_email,
            'phone': student_phone,
            'class_level': student_class_level,
            'student_number': student_student_number,
        }

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Student.objects.first().first_name,
                          student_first_name)
        self.assertEquals(Student.objects.first().middle_name,
                          student_middle_name)
        self.assertEquals(Student.objects.first().last_name, student_last_name)
        self.assertEquals(Student.objects.first().phone, student_phone)
        self.assertEquals(Student.objects.first().email,  student_email)
        self.assertEquals(Student.objects.first().school, student_school)
        self.assertEquals(Student.objects.first().class_level,
                          student_class_level)
        self.assertEquals(Student.objects.first(
        ).student_number, student_student_number)

    def test_teacher_update_student_POST_no_data_does_not_update_student(self):
        self.client.login(username='teacher', password='password')
        url = reverse('update_student', args=[self.student.id])

        student_first_name = self.student.first_name
        student_middle_name = self.student.middle_name
        student_last_name = self.student.last_name
        student_phone = self.student.phone
        student_email = self.student.email
        student_school = self.student.school
        student_class_level = self.student.class_level
        student_student_number = self.student.student_number

        data = {}

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(Student.objects.first().first_name,
                          student_first_name)
        self.assertEquals(Student.objects.first().middle_name,
                          student_middle_name)
        self.assertEquals(Student.objects.first().last_name, student_last_name)
        self.assertEquals(Student.objects.first().phone, student_phone)
        self.assertEquals(Student.objects.first().email,  student_email)
        self.assertEquals(Student.objects.first().school, student_school)
        self.assertEquals(Student.objects.first().class_level,
                          student_class_level)
        self.assertEquals(Student.objects.first(
        ).student_number, student_student_number)

    def test_teacher_update_subject_class_POST_updates_subject_class(self):
        self.client.login(username='teacher', password='password')
        url = reverse('update_subject_class', args=[self.subject_class.id])

        subject = Subject.objects.create(name='New subject')
        subject_class_class_level = 10
        subject_class_subject = subject

        data = {
            'class_level': subject_class_class_level,
            'subject': subject_class_subject.id,
        }

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(SubjectClass.objects.first(
        ).class_level, subject_class_class_level)
        self.assertEquals(SubjectClass.objects.first().subject,
                          subject_class_subject)

    def test_teacher_update_subject_class_POST_no_data_does_not_update_subject_class(self):
        self.client.login(username='teacher', password='password')

        url = reverse('update_subject_class', args=[self.subject_class.id])

        subject_class_class_level = self.subject_class.class_level
        subject_class_subject = self.subject_class.subject

        data = {}

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(SubjectClass.objects.first(
        ).class_level, subject_class_class_level)
        self.assertEquals(SubjectClass.objects.first().subject,
                          subject_class_subject)

    def test_teacher_update_grade_POST_updates_grade(self):
        self.client.login(username='teacher', password='password')

        grade_number = 4
        grade_student = self.student
        grade_subject_class = self.subject_class
        grade_term = self.summer_term

        grade = Grade.objects.create(
            number=grade_number, student=grade_student, subject_class=grade_subject_class, term=grade_term)

        url = reverse('update_grade', args=[grade.id])

        grade_update_number = 6
        data = {
            'number': grade_update_number,
        }

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Grade.objects.first().number, grade_update_number)
        self.assertEquals(Grade.objects.first().student, grade_student)
        self.assertEquals(Grade.objects.first().subject_class,
                          grade_subject_class)
        self.assertEquals(Grade.objects.first().term, grade_term)

    def test_teacher_update_grade_POST_no_data_does_not_update_grade(self):
        self.client.login(username='teacher', password='password')

        grade_number = 4
        grade_student = self.student
        grade_subject_class = self.subject_class
        grade_term = self.summer_term

        grade = Grade.objects.create(
            number=grade_number, student=grade_student, subject_class=grade_subject_class, term=grade_term)

        url = reverse('update_grade', args=[grade.id])
        data = {}

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(Grade.objects.first().number, grade_number)
        self.assertEquals(Grade.objects.first().student, grade_student)
        self.assertEquals(Grade.objects.first().subject_class,
                          grade_subject_class)
        self.assertEquals(Grade.objects.first().term, grade_term)

    def test_teacher_update_absence_POST_update_absence(self):
        self.client.login(username='teacher', password='password')

        date_today = date.today()
        absence_date = date_today
        absence_excused = False
        absence_subject_class = self.subject_class
        absence_student = self.student
        absence_term = self.summer_term

        absence = Absence.objects.create(date=absence_date, excused=absence_excused,
                                         subject_class=absence_subject_class, student=absence_student, term=absence_term)

        url = reverse('update_absence', args=[absence.id])

        updated_absence_excused = True
        updated_absence_term = self.winter_term

        data = {
            'date': absence_date,
            'excused': True,
            'subject_class': absence_subject_class.id,
            'student': absence_student.id,
            'term': updated_absence_term.id,
        }

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Absence.objects.first().date, absence_date)
        self.assertEquals(Absence.objects.first().excused,
                          updated_absence_excused)
        self.assertEquals(Absence.objects.first(
        ).subject_class, absence_subject_class)
        self.assertEquals(Absence.objects.first().student, absence_student)
        self.assertEquals(Absence.objects.first().term, updated_absence_term)

    def test_teacher_update_absence_POST_no_data_does_not_update_absence(self):
        self.client.login(username='teacher', password='password')

        date_today = date.today()
        absence_date = date_today
        absence_excused = False
        absence_subject_class = self.subject_class
        absence_student = self.student
        absence_term = self.summer_term

        absence = Absence.objects.create(date=absence_date, excused=absence_excused,
                                         subject_class=absence_subject_class, student=absence_student, term=absence_term)

        url = reverse('update_absence', args=[absence.id])
        data = {}

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(Absence.objects.first().date, absence_date)
        self.assertEquals(Absence.objects.first().excused, absence_excused)
        self.assertEquals(Absence.objects.first(
        ).subject_class, absence_subject_class)
        self.assertEquals(Absence.objects.first().student, absence_student)
        self.assertEquals(Absence.objects.first().term, absence_term)

    def test_teacher_update_remark_POST_updates_remark(self):
        self.client.login(username='teacher', password='password')

        remark_content = 'Some content'
        remark_student = self.student
        remark_teacher = self.teacher
        remark_term = self.winter_term

        remark = Remark.objects.create(content=remark_content, student=remark_student,
                                       teacher=remark_teacher, term=remark_term)

        url = reverse('update_remark', args=[remark.id])

        remark_updated_content = 'Updated content'
        remark_updated_term = self.summer_term
        data = {
            'content': remark_updated_content,
            'student': remark_student.id,
            'teacher': remark_teacher.id,
            'term': remark_updated_term.id,
        }

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Remark.objects.first().content,
                          remark_updated_content)
        self.assertEquals(Remark.objects.first().student, remark_student)
        self.assertEquals(Remark.objects.first().teacher, remark_teacher)
        self.assertEquals(Remark.objects.first().term, remark_updated_term)

    def test_teacher_update_remark_POST_no_data_does_not_update_remark(self):
        self.client.login(username='teacher', password='password')

        remark_content = 'Some content'
        remark_student = self.student
        remark_teacher = self.teacher
        remark_term = self.winter_term

        remark = Remark.objects.create(content=remark_content, student=remark_student,
                                       teacher=remark_teacher, term=remark_term)

        url = reverse('update_remark', args=[remark.id])
        data = {}

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(Remark.objects.first().content, remark_content)
        self.assertEquals(Remark.objects.first().student, remark_student)
        self.assertEquals(Remark.objects.first().teacher, remark_teacher)
        self.assertEquals(Remark.objects.first().term, remark_term)

    def test_teacher_update_praise_POST_updates_praise(self):
        self.client.login(username='teacher', password='password')

        praise_content = 'Some content'
        praise_student = self.student
        praise_teacher = self.teacher
        praise_term = self.winter_term

        praise = Praise.objects.create(content=praise_content, student=praise_student,
                                       teacher=praise_teacher, term=praise_term)

        url = reverse('update_praise', args=[praise.id])

        praise_updated_content = 'Updated content'
        praise_updated_term = self.summer_term
        data = {
            'content': praise_updated_content,
            'student': praise_student.id,
            'teacher': praise_teacher.id,
            'term': praise_updated_term.id,
        }

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Praise.objects.first().content,
                          praise_updated_content)
        self.assertEquals(Praise.objects.first().student, praise_student)
        self.assertEquals(Praise.objects.first().teacher, praise_teacher)
        self.assertEquals(Praise.objects.first().term, praise_updated_term)

    def test_teacher_update_praise_POST_no_data_does_not_update_praise(self):
        self.client.login(username='teacher', password='password')

        praise_content = 'Some content'
        praise_student = self.student
        praise_teacher = self.teacher
        praise_term = self.winter_term

        praise = Praise.objects.create(content=praise_content, student=praise_student,
                                       teacher=praise_teacher, term=praise_term)

        url = reverse('update_praise', args=[praise.id])
        data = {}

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(Praise.objects.first().content, praise_content)
        self.assertEquals(Praise.objects.first().student, praise_student)
        self.assertEquals(Praise.objects.first().teacher, praise_teacher)
        self.assertEquals(Praise.objects.first().term, praise_term)

    def test_teacher_remove_grade_POST_removes_grade(self):
        self.client.login(username='teacher', password='password')

        grade_number = 4
        grade_student = self.student
        grade_subject_class = self.subject_class
        grade_term = self.summer_term

        grade = Grade.objects.create(
            number=grade_number, student=grade_student, subject_class=grade_subject_class, term=grade_term)

        grades_count_after_creating_grade = Grade.objects.all().count()

        url = reverse('delete_grade', args=[grade.id])

        response = self.client.post(url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Grade.objects.all().count(), 0)
        self.assertNotEquals(Grade.objects.all().count(),
                             grades_count_after_creating_grade)

    def test_teacher_remove_absence_POST_removes_absence(self):
        self.client.login(username='teacher', password='password')

        date_today = date.today()
        absence_date = date_today
        absence_excused = False
        absence_subject_class = self.subject_class
        absence_student = self.student
        absence_term = self.summer_term

        absence = Absence.objects.create(date=absence_date, excused=absence_excused,
                                         subject_class=absence_subject_class, student=absence_student, term=absence_term)

        absences_count_after_creating_absence = Absence.objects.all().count()

        url = reverse('delete_absence', args=[absence.id])

        response = self.client.post(url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Absence.objects.all().count(), 0)
        self.assertNotEquals(Absence.objects.all().count(),
                             absences_count_after_creating_absence)

    def test_teacher_remove_remark_POST_removes_remark(self):
        self.client.login(username='teacher', password='password')

        remark_content = 'Some content'
        remark_student = self.student
        remark_teacher = self.teacher
        remark_term = self.winter_term

        remark = Remark.objects.create(content=remark_content, student=remark_student,
                                       teacher=remark_teacher, term=remark_term)

        remarks_count_after_creating_remark = Remark.objects.all().count()

        url = reverse('delete_remark', args=[remark.id])

        response = self.client.post(url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Remark.objects.all().count(), 0)
        self.assertNotEquals(Remark.objects.all().count(),
                             remarks_count_after_creating_remark)

    def test_teacher_remove_praise_POST_removes_praise(self):
        self.client.login(username='teacher', password='password')

        praise_content = 'Some content'
        praise_student = self.student
        praise_teacher = self.teacher
        praise_term = self.winter_term

        praise = Praise.objects.create(content=praise_content, student=praise_student,
                                       teacher=praise_teacher, term=praise_term)

        praises_count_after_creating_remark = Praise.objects.all().count()

        url = reverse('delete_praise', args=[praise.id])

        response = self.client.post(url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Praise.objects.all().count(), 0)
        self.assertNotEquals(Praise.objects.all().count(),
                             praises_count_after_creating_remark)
