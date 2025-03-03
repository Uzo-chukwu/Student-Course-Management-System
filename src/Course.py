class Course:
    def __init__(self, course_title, course_code):
        self.__course_title = course_title
        self.__course_code = course_code

    @property
    def get_course_title(self):
        return self.__course_title
    @property
    def get_course_code(self):
        return self.__course_code

