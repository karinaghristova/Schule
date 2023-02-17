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


class TestTeacherUrls(SimpleTestCase):
    def test_teacher_account_url_is_resolved(self):
        url = reverse('teacher_account')
        self.assertEquals(resolve(url).func, teacher_account)

    def test_teacher_students_url_is_resolved(self):
        url = reverse('students')
        self.assertEquals(resolve(url).func, teacher_students)

    def test_teacher_parents_url_is_resolved(self):
        url = reverse('parents')
        self.assertEquals(resolve(url).func, teacher_parents)

    def test_teacher_subjects_url_is_resolved(self):
        url = reverse('teacher_subjects')
        self.assertEquals(resolve(url).func, teacher_subjects)

    def test_subject_class_detail_url_is_resolved(self):
        url = reverse('subject_class_detail', args=['some_pk'])
        self.assertEquals(resolve(url).func, teacher_subject_class_detail)

    def test_teacher_absences_url_is_resolved(self):
        url = reverse('teacher_absences')
        self.assertEquals(resolve(url).func, teacher_absences)

    def test_teacher_remarks_url_is_resolved(self):
        url = reverse('teacher_remarks')
        self.assertEquals(resolve(url).func, teacher_remarks)

    def test_teacher_praises_url_is_resolved(self):
        url = reverse('teacher_praises')
        self.assertEquals(resolve(url).func, teacher_praises)

    # Create urls start
    def test_add_child_to_parent_url_is_resolved(self):
        url = reverse('add_child_to_parent', args=['some_pk'])
        self.assertEquals(resolve(url).func, teacher_assign_student_to_parent)

    def test_create_subject_url_is_resolved(self):
        url = reverse('create_subject')
        self.assertEquals(resolve(url).func, teacher_create_subject)

    def test_create_subject_class_url_is_resolved(self):
        url = reverse('create_subject_class')
        self.assertEquals(resolve(url).func, teacher_create_subject_class)

    def test_create_grade_url_is_resolved(self):
        url = reverse('create_grade', args=['some_pk'])
        self.assertEquals(resolve(url).func, teacher_create_grade_for_student)

    def test_add_absence_url_is_resolved(self):
        url = reverse('add_absence', args=['some_pk'])
        self.assertEquals(resolve(url).func, teacher_create_absence)

    def test_create_remark_url_is_resolved(self):
        url = reverse('create_remark')
        self.assertEquals(resolve(url).func, teacher_create_remark)

    def test_create_praise_url_is_resolved(self):
        url = reverse('create_praise')
        self.assertEquals(resolve(url).func, teacher_create_praise)
    # Create urls end

    # Update urls start
    def test_teacher_update_info_url_is_resolved(self):
        url = reverse(teacher_update_info)
        self.assertEquals(resolve(url).func, teacher_update_info)

    def test_update_student_url_is_resolved(self):
        url = reverse('update_student', args=['some_pk'])
        self.assertEquals(resolve(url).func, teacher_update_student)

    def test_update_subject_class_url_is_resolved(self):
        url = reverse('update_subject_class', args=['some_pk'])
        self.assertEquals(resolve(url).func, teacher_update_subject_class)

    def test_update_grade_url_is_resolved(self):
        url = reverse('update_grade', args=['some_pk'])
        self.assertEquals(resolve(url).func, teacher_update_grade)

    def test_update_absence_url_is_resolved(self):
        url = reverse('update_absence', args=['some_pk'])
        self.assertEquals(resolve(url).func, teacher_update_absence)

    def test_update_remark_url_is_resolved(self):
        url = reverse('update_remark', args=['some_pk'])
        self.assertEquals(resolve(url).func, teacher_update_remark)

    def test_update_praise_url_is_resolved(self):
        url = reverse('update_praise', args=['some_pk'])
        self.assertEquals(resolve(url).func, teacher_update_praise)

    def test_add_students_to_subject_class_url_is_resolved(self):
        url = reverse('add_students_to_subject_class', args=['some_pk'])
        self.assertEquals(resolve(url).func,
                          teacher_edit_students_to_subject_class)
    # Update urls end

    # Delete urls start
    def test_delete_grade_url_is_resolved(self):
        url = reverse('delete_grade', args=['some_pk'])
        self.assertEquals(resolve(url).func, teacher_remove_grade)

    def test_delete_absence_url_is_resolved(self):
        url = reverse('delete_absence', args=['some_pk'])
        self.assertEquals(resolve(url).func, teacher_remove_absence)

    def test_delete_remark_url_is_resolved(self):
        url = reverse('delete_remark', args=['some_pk'])
        self.assertEquals(resolve(url).func, teacher_remove_remark)

    def test_delete_praise_url_is_resolved(self):
        url = reverse('delete_praise', args=['some_pk'])
        self.assertEquals(resolve(url).func, teacher_remove_praise)

    def test_delete_subject_class_url_is_resolved(self):
        url = reverse('delete_subject_class', args=['some_pk'])
        self.assertEquals(resolve(url).func, teacher_remove_subject_class)


class TestParentUrls(SimpleTestCase):
    def test_parent_account_url_is_resolved(self):
        url = reverse('parent_account')
        self.assertEquals(resolve(url).func, parent_account)

    def test_parent_grades_url_is_resolved(self):
        url = reverse('parent_grades')
        self.assertEquals(resolve(url).func, parent_grades)

    def test_parent_absences_url_is_resolved(self):
        url = reverse('parent_absences')
        self.assertEquals(resolve(url).func, parent_absences)

    def test_parent_remarks_url_is_resolved(self):
        url = reverse('parent_remarks')
        self.assertEquals(resolve(url).func, parent_remarks)

    def test_parent_praises_url_is_resolved(self):
        url = reverse('parent_praises')
        self.assertEquals(resolve(url).func, parent_praises)

    def test_parent_update_info_url_is_resolved(self):
        url = reverse('parent_update_info')
        self.assertEquals(resolve(url).func, parent_update_info)


