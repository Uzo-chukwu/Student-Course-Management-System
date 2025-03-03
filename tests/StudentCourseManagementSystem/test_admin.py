import unittest
from src.StudentCourseManagementSystem.Facilitator import Facilitator
from src.StudentCourseManagementSystem.Admin import Admin

class AdminTest(unittest.TestCase):
    def test_admin_exists(self):
        my_admin = Admin("John", "123BD", "john123@gmail.com", "0000" )

    def test_create_admin(self):
        my_admin = Admin("John", "123BD", "john123@gmail.com", "0000")

    def test_that_facilitator_is_created_successfully(self):
        my_admin = Admin("John", "123BD", "john123@gmail.com", "0000")
        my_admin.create_facilitator("John", "123BD", "john123@gmail.com", "0000", "Python", 101)
        self.assertEqual(my_admin.get_facilitator_size(), 1)

    # def test_that_more_facilitator_created_successfully(self):
    #     my_admin = Admin("John", "123BD", "john123@gmail.com", "0000")
    #     my_admin.create_facilitator("John", "123BD", "john123@gmail.com", "0000", "Python")
    #     self.assertEqual(my_admin.get_facilitator_size(), 1)
    #
    #
    # def test_that_two_facilitator_created_successfully(self):
    #     my_admin = Admin("John", "123BD", "john123@gmail.com", "0000")
    #     my_admin.create_facilitator("John", "123BD", "john123@gmail.com", "0000", "Python")
    #     self.assertEqual(my_admin.get_facilitator_size(), 1)
    #
    #     my_admin.create_facilitator("Stephen", "123BJ", "stephen123@gmail.com", "2020", "Python")
    #     self.assertEqual(my_admin.get_facilitator_size(), 2)
    #
    # def test_three_facilitator_created_successfully(self):
    #     my_admin = Admin("John", "123BD", "john123@gmail.com", "0000")
    #     my_admin.create_facilitator("John", "123BD", "john123@gmail.com", "0000", "Python")
    #     self.assertEqual(my_admin.get_facilitator_size(), 1)
    #
    #     my_admin.create_facilitator("Stephen", "123BJ", "stephen123@gmail.com", "2020", "Python")
    #     self.assertEqual(my_admin.get_facilitator_size(), 2)
    #
    #
    #     my_admin.create_facilitator("Mark", "290GJ", "mark123@gmail.com", "2456", "Python")
    #     self.assertEqual(my_admin.get_facilitator_size(), 3)

    def test_that_admin_has_list_course_when_created_by_facilitator(self):
        my_admin = Admin("John", "123BD", "john123@gmail.com", "0000")
        my_admin.create_facilitator("John", "123BD", "john123@gmail.com", "0000", "Python", 101)
        my_admin.create_facilitator("Mark", "241D", "mark123@gmail.com", "111", "Java", 111)

        for facilitator in my_admin.get_facilitators():
            value = None
            facilitator.create_course(facilitator.get_course_name, facilitator.get_course_id)
            for course in facilitator.get_courses():
                value = course.get_course_title

            self.assertEqual(facilitator.get_course_name, value)










