

from models.user import User
import re

class Student(User):
    def __init__(self, user_id: int, username: str, password: str, email: str):
        super().__init__(user_id, username, password, role = "student", email = email)
        self.enrolled_courses = {}  # {course_id: grade}

    def enroll_course(self, course_id: int):
        self.enrolled_courses[course_id] = None  # No grade initially


    def view_instructor(self, course_id: int, course_manager):
        course = course_manager.get_course(course_id)
        if course_id in self.enrolled_courses:
            return course.instructor
        return "Not enrolled in this course."

    def verify_email(self, email: str) -> bool:
        email_validator = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_validator, email) is not None

    def is_email_matching(self, email:str) -> bool:
        return self.email == email


    def view_grades(self):
        return self.enrolled_courses

    def __eq__(self, other):
        if isinstance(other, Student):
            self.user_id = other.user_id
            return False


    def __str__(self):
        return f"(ID: {self.user_id}\n, Username: {self.username})"