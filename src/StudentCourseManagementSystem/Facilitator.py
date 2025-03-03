from src.Course import Course
from src.StudentCourseManagementSystem.user import User



class Facilitator(User):

    course = []
    def __init__(self, user_name, user_id, email, password, course_name, course_id):
        super().__init__(user_name, user_id, email, password)
        self.__course_name = course_name
        self.__course_id = course_id

    def create_course(cls, course_title, course_code):
        new_course = Course(course_title, course_code)
        cls.course.append(new_course)




    @classmethod
    def get_courses(cls):
        return cls.course

    def get_course_size(cls):
        return len(cls.course)

    @property
    def get_course_name(self):
        return self.__course_name
    @property
    def get_course_id(self):
        return self.__course_id





# course = Course("Python", 101)
# course.create_course(cls, course_title, course_code)

# print(course.get_course_size())


