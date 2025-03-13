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

        if self.get_course_size() > 0:
            raise CourseAlreadyCreatedException(f"An instructor can only create one course for this semester\nYou have already created this {self.taught_courses[0]}")
        course = Course(course_id, name, self.username, credits)
        course_manager.add_course(course)
        self.taught_courses.append(course_id)

    def view_students(self, course_id: int, course_manager):
        return course_manager.get_students_in_course(course_id)

    def grade_student(self, student_id: int, course_id: int, grade: str, course_manager):

        # if not self.taught_courses:
        #     return f"You have not created any course!\nKindly create a course first!"

        if course_id not in self.taught_courses:
            return f"Course id {course_id} does not exist\nOr you are not the instructor of this course!"

        student = course_manager.get_student(student_id)

        if not student:
            return f"Student {student_id} cannot be found"

        if int(course_id) in map(int, student.enrolled_courses.keys()):
            student.enrolled_courses[course_id] = grade
            return f"Graded {student.username} with {grade} in course {course_id}."
        return "Student not enrolled in this course."

    def __eq__(self, other):
        if isinstance(other, Instructor):
            self.user_id = other.user_id
            return False


    def best_student(self, course_id: int, course_manager):
        students = course_manager.get_students_in_course(course_id)
        if not students:
            return f"No students in course {course_id}"
        graded_student = {person.username: person.enrolled_courses[course_id] for person in students if
                          person.enrolled_courses[course_id] is not None}
        if not graded_student:
            return f"No students has been graded in {course_manager.name}: {course_id} yet"


        best_student = max(graded_student, key=graded_student.get)
        return f"Best student is: {best_student} ({graded_student[best_student]})"

    def worst_student(self, course_id: int, course_manager):
        students = course_manager.get_students_in_course(course_id)
        if not students:
            return f"No students in course {course_id}"
        graded_student = {person.username: person.enrolled_courses[course_id] for person in students if
                          person.enrolled_courses[course_id] is not None}
        if not graded_student:
            return f"No students has been graded in {course_manager.name}: {course_id} yet"

        worst_student = min(graded_student, key=graded_student.get)
        return f"Worst student is: {worst_student} ({graded_student[worst_student]})"

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