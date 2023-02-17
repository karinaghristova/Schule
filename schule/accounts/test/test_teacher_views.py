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

    def test_teacher_account_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_update_info_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_students_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_subjects_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_parents_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_subject_class_detail_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_absences_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_remarks_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_praises_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_assign_student_to_parent_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_create_subject_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_create_subject_class_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_create_grade_for_student_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_create_absence_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_create_remark_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_create_praise_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_update_student_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_update_subject_class_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_update_grade_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_update_absence_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_update_remark_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_update_praise_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_remove_absence_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_remove_grade_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_remove_remark_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_remove_praise_view_is_accessible_for_users_with_group_teacher_only(self):
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

    def test_teacher_remove_subject_class_view_is_accessible_for_users_with_group_teacher_only(self):
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
