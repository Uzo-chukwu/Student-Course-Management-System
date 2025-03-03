import unittest
from src.StudentCourseManagementSystem.Facilitator import Facilitator

class FacilitatorTest(unittest.TestCase):
    def test_facilitator_creates_course(self):
        my_facilitator = Facilitator("John", "123BD", "john123@gmail.com", "0000", "Python", 101)
        my_facilitator.create_course("Python", 101)
        self.assertEqual(my_facilitator.get_course_size(), 1)