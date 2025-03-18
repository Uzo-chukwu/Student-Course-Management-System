
from models.course import Course
from models.user import User
import re

class UsedIdException(Exception):
    pass


class CourseAlreadyCreatedException(Exception):
    pass


class Instructor(User):
    def __init__(self, user_id:int, username: str, password: str, email:str):
        super().__init__(user_id, username, password, role = "instructor", email = email)
        self.taught_courses = []  # List of course IDs

    def create_course(self, course_id: int, name: str, credits: int, course_manager):
        from managers.course_manager import RepeatedCourseCreationException

        if self.get_course_size() > 0:
            raise CourseAlreadyCreatedException(f"An instructor can only create one course for this semester\nYou have already created this {self.taught_courses[0]}")

        if any(course.course_id == course_id for course in course_manager.courses):
            raise RepeatedCourseCreationException("Course already created!")
        course = Course(course_id, name, self.username, credits)
        course.instructor = self
        course_manager.add_course(course)
        self.taught_courses.append(course_id)
        course_manager.save_to_file()

    def view_students(self, course_id: int, course_manager):
        return course_manager.get_students_in_course(course_id)


    def grade_student(self, student_id: int, course_id: int, grade: str, course_manager):
        if course_id not in self.taught_courses:
            return False, f"Course id {course_id} does not exist\nOr you are not the instructor of this course!"

        student = course_manager.get_student(student_id)

        if not student:
            return False, f"Student {student_id} cannot be found"

        if course_id in student.enrolled_courses:

            student.enrolled_courses[course_id] = grade
            course_manager.save_to_file()
            return True, f"Graded {student.username} with {grade} in course {course_id}."
        else:
            return False, f"Student not enrolled in this course yet!"

    def __eq__(self, other):
        if isinstance(other, Instructor):
            self.user_id == other.user_id
            return False



    def best_student(self, course_id: int, course_manager):
        if course_id not in self.taught_courses:
            return f"Access denied!\nYou are not the instructor of this course"
        students = course_manager.get_students_in_course(course_id)
        if not students:
            return f"No students in course {course_id}"
        graded_student = {person.username: int(person.enrolled_courses[course_id]) for person in students if
                          person.enrolled_courses[course_id] is not None}
        if not graded_student:
            return f"No students has been graded in {course_manager.get_course(course_id).name}: {course_id} yet"


        best_student = max(graded_student, key=graded_student.get)
        return f"Best student is: {best_student} ({graded_student[best_student]})"

    def worst_student(self, course_id: int, course_manager):
        if course_id not in self.taught_courses:
            return f"Access denied!\nYou are not the instructor of this course"
        students = course_manager.get_students_in_course(course_id)
        if not students:
            return f"No students in course {course_id}"
        graded_student = {person.username: int(person.enrolled_courses[course_id]) for person in students if
                          person.enrolled_courses[course_id] is not None}
        if not graded_student:
            return f"No students has been graded in {course_manager.get_course(course_id).name}: {course_id} yet"

        worst_student = min(graded_student, key=graded_student.get)
        return f"Worst student is: {worst_student} ({graded_student[worst_student]})"



    def get_students_performance_chart(self, course_manager):
        if not self.taught_courses:
            return f"Instructor cannot be found!"
        course_id = self.taught_courses[0]
        enrolled_student = course_manager.get_students_in_course(course_id)

        if not enrolled_student:
            return f"No student enrolled in your course!"

        student = ""
        grade = 0
        bar_chart = ""
        performance_status = ""
        performance_list = []

        for student in enrolled_student:
            grade = student.enrolled_courses.get(course_id, None)

            if grade is None:
                performance_list.append(f"Student has not been graded yet!")
                continue

            bar_length = grade//10
            bar_chart = "*" * bar_length
            performance_status = "PASS ✅" if grade >= 50 else "FAIL ❌️"

            performance_list.append(f"Student: {student.username} | Grade: {grade} | {bar_chart}: {performance_status}")

        return "\n".join(performance_list)



    def get_course_size(self):
        return len(self.taught_courses)

    def verify_email(self, email: str) -> bool:
        email_validator = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_validator, email) is not None

    def is_email_matching(self, email:str) -> bool:
        return self.email == email
    
    def has_created_course(self):
        return len(self.taught_courses) > 0


    def __str__(self):
        return f"Instructor(ID: {self.user_id}, Username: {self.username})"