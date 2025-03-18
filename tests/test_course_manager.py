import unittest


from managers.course_manager import CourseManager, RepeatedCourseCreationException
from models.course import Course
from models.instructor import Instructor
from models.student import Student



class InvalidEmailException(Exception):
    pass


class TestCourseManager(unittest.TestCase):
    my_manager = CourseManager()
    my_student = Student(1, "John", "0000", "chrisoj@gmail.com")
    def test_student_can_be_added_to_managers_list(self):
        my_manager = CourseManager()
        my_student = Student(1, "John", "0000", "chrisoj@gmail.com")
        my_manager.add_student(my_student)
        self.assertEqual(my_manager.get_size_of_students, 1)

    def test_more_student_can_be_added_to_managers_list(self):
        my_manager = CourseManager()
        my_student = Student(1, "John", "0000", "chrisoj@gmail.com")
        my_manager.add_student(my_student)
        self.assertEqual(my_manager.get_size_of_students, 1)

        my_student2 = Student(0, "Stephen", "2020", "stephen@gmail.com")
        my_manager.add_student(my_student2)
        self.assertEqual(my_manager.get_size_of_students, 2)

    def test_instructor_can_be_added_to_managers_list(self):
        my_manager = CourseManager()
        my_instructor = Instructor(1, "John", "0000", "chrisoj@gmail.com")
        my_manager.add_instructor(my_instructor)
        self.assertEqual(my_manager.get_size_of_instructor, 1)

    def test_more_instructor_can_be_added_to_managers_list(self):
        my_manager = CourseManager()
        my_instructor1 = Instructor(1, "John", "0000", "chrisoj@gmail.com")
        my_manager.add_instructor(my_instructor1)
        self.assertEqual(my_manager.get_size_of_instructor, 1)

        my_instructor2 = Instructor(2, "Chris", "1212", "mark@gmail.com")
        my_manager.add_instructor(my_instructor2)
        self.assertEqual(my_manager.get_size_of_instructor, 2)

    def test_instructor_creates_course(self):
        my_manager = CourseManager()
        my_instructor = Instructor(1, "John", "0000", "chrisoj@gmail.com")
        my_manager.add_instructor(my_instructor)
        my_instructor.create_course(1, "Python", 4, my_manager)
        self.assertEqual(my_manager.get_size_of_course, 1)

    def test_manager_display_all_courses(self):
        my_manager = CourseManager()
        my_instructor = Instructor(1, "John", "0000", "chrisoj@gmail.com")
        my_manager.add_instructor(my_instructor)
        my_instructor.create_course(1, "Python", 4, my_manager)
        self.assertEqual(my_manager.get_size_of_course, 1)

        my_instructor = Instructor(1, "John", "0000", "chrisoj@gmail.com")
        my_manager.add_instructor(my_instructor)
        my_instructor.create_course(2, "Java", 4, my_manager)
        self.assertEqual(my_manager.get_size_of_course, 2)

        my_instructor = Instructor(3, "Mark", "2020", "mark@gmail.com")
        my_manager.add_instructor(my_instructor)
        my_instructor.create_course(3, "JavaScript", 3, my_manager)
        self.assertEqual(my_manager.get_size_of_course, 3)

    def test_cause_created_more_than_once_raises_exception(self):
        my_manager = CourseManager()
        my_instructor = Instructor(1, "John", "0000", "chrisoj@gmail.com")
        my_manager.add_instructor(my_instructor)
        my_instructor.create_course(1, "Python", 4, my_manager)
        self.assertEqual(my_manager.get_size_of_course, 1)

        my_instructor = Instructor(1, "John", "0000", "chrisoj@gmail.com")
        my_manager.add_instructor(my_instructor)
        with self.assertRaises(RepeatedCourseCreationException):
            my_instructor.create_course(1, "Python", 4, my_manager)

    def test_exception_is_raised_for_invalid_email(self):
        my_manager = CourseManager()
        with self.assertRaises(InvalidEmailException):
            my_manager.add_instructor(Instructor(1, "John", "0000", "chrisoj"))


    def test_student_can_enroll_in_a_course(self):
        my_manager = CourseManager()
        my_student = Student(1, "Stephen", "2020", "stephen@gmail.com")
        my_manager.add_student(my_student)
        my_instructor = Instructor(1, "John", "0000", "chrisoj@gmail.com")
        my_manager.add_instructor(my_instructor)

        my_instructor.create_course(404, "Python", 4, my_manager)
        my_student.enroll_course(404)
        self.assertIn(404, my_student.enrolled_courses)
        self.assertIsNone(my_student.enrolled_courses[404])

    def test_student_can_enroll_in_more_than_one_course(self):
        my_manager = CourseManager()
        my_student = Student(1, "Stephen", "2020", "stephen@gmail.com")
        my_manager.add_student(my_student)
        my_instructor1 = Instructor(1, "John", "0000", "chrisoj@gmail.com")
        my_manager.add_instructor(my_instructor1)

        my_instructor1.create_course(404, "Python", 4, my_manager)
        my_student.enroll_course(404)
        self.assertIn(404, my_student.enrolled_courses)

        my_instructor2 = Instructor(2, "Chris", "1212", "mark@gmail.com")
        my_manager.add_instructor(my_instructor2)
        my_instructor2.create_course(100, "Java", 4, my_manager)
        my_student.enroll_course(100)
        self.assertIn(100, my_student.enrolled_courses)
        self.assertIsNone(my_student.enrolled_courses[404])
        self.assertIsNone(my_student.enrolled_courses[100])

    def test_instructor_can_view_students_in_course(self):
        my_manager = CourseManager()


        my_manager.students.clear()
        my_manager.courses.clear()
        my_manager.instructors.clear()
        my_manager.enrollments.clear()

        my_instructor = Instructor(1, "Chris", "1212", "mark@gmail.com")
        my_manager.add_instructor(my_instructor)
        my_instructor.create_course(200, "JavaScript", 4, my_manager)

        my_student1 = Student(1, "Stephen", "2020", "stephen@gmail.com")
        my_student2 = Student(2, "Mary", "1212", "mary@gmail.com")

        my_manager.add_student(my_student1)
        my_manager.add_student(my_student2)


        my_manager.enroll_student(1, 200)
        my_manager.enroll_student(2, 200)



        print(my_manager.get_students_in_course(200))

        students_in_course = my_instructor.view_students(200, my_manager)
        for student in students_in_course:
            print(student)
        self.assertIn(my_student1, students_in_course)
        self.assertIn(my_student2, students_in_course)
        self.assertEqual(len(students_in_course), 2)

    def test_that_student_can_view_the_list_of_courses(self):
        my_manager = CourseManager()

        my_manager.students.clear()
        my_manager.courses.clear()
        my_manager.instructors.clear()
        my_manager.enrollments.clear()

        my_instructorOne = Instructor(1, "Chris", "1212", "mark@gmail.com")
        my_manager.add_instructor(my_instructorOne)

        my_instructorTwo = Instructor(2, "Max", "1212", "dark@gmail.com")
        my_manager.add_instructor(my_instructorTwo)

        my_instructorThree = Instructor(3, "Sam", "1212", "hark@gmail.com")
        my_manager.add_instructor(my_instructorThree)

        my_instructorOne.create_course(200, "Java", 4, my_manager)
        my_instructorTwo.create_course(201, "Python", 4, my_manager)
        my_instructorThree.create_course(202, "JavaScript", 4, my_manager)


        my_student = Student(1, "Stephen", "2020", "stephen@gmail.com")
        my_manager.add_student(my_student)

        my_manager.enroll_student(1, 200)
        my_manager.enroll_student(1, 201)
        my_manager.enroll_student(1, 202)

        courseOne = my_manager.get_course(200)
        courseTwo = my_manager.get_course(201)
        courseThree = my_manager.get_course(202)

        print(courseOne)
        print(courseTwo)
        print(courseThree)
        self.assertIsNotNone(courseOne)
        self.assertIsNotNone(courseTwo)
        self.assertIsNotNone(courseThree)
        self.assertTrue(any(enrollment.student_id == 1 and enrollment.course_id == 200 for enrollment in my_manager.enrollments))
        self.assertTrue(any(enrollment.student_id == 1 and enrollment.course_id == 201 for enrollment in my_manager.enrollments))
        self.assertTrue(any(enrollment.student_id == 1 and enrollment.course_id == 202 for enrollment in my_manager.enrollments))

    def test_instructor_can_grade_students_in_course(self):
        pass









