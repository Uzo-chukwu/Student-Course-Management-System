from managers import course_manager
from models.user import User
import re

class Student(User):
    def __init__(self, user_id: int, username: str, password: str, email: str):
        super().__init__(user_id, username, password, role = "student", email = email)
        self.enrolled_courses = {}  # {course_id: grade}

    def enroll_course(self, course_id: int):
        if course_id not in self.enrolled_courses:
            self.enrolled_courses[course_id] = None  # No grade initially
        else:
            print(f"Student {self.username} with id {self.user_id} already enrolled in course {course_id}")


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


    def view_grades(self, course_id: int, course_manager):
        if not self.enrolled_courses:
            return f"You are not enrolled in this course."

        if course_id not in self.enrolled_courses:
            return f"You are not enrolled in this course {course_id}"
        # grade_record = []
        # for course_id, grade in self.enrolled_courses.items():
        course = course_manager.get_course(course_id)
        course_name = course.name if course else "This course in not known"
        grade = self.enrolled_courses.get(course_id, None)
        grade_display = grade if grade is not None else "Grade not assigned yet!"
        # grade_record.append(f"{course_name}: {grade_display}")

            # return self.enrolled_courses
        # return "\n".join(grade_record)
        return f"{course_name}: {grade_display}"

    def get_all_enrolled_courses(self, course_manager):
        enrolled_courses = []
        for course_id in self.enrolled_courses:
            course = course_manager.get_course(course_id)
            if course:
                enrolled_courses.append(course)
        return enrolled_courses

    def __eq__(self, other):
        if isinstance(other, Student):
            self.user_id = other.user_id
            return False


    def __str__(self):
        return f"(ID: {self.user_id}\n, Username: {self.username})"
