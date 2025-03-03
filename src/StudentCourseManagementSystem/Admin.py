from src.StudentCourseManagementSystem.user import User
from src.StudentCourseManagementSystem.Facilitator import Facilitator
class Admin(User):
    facilitators = []
    courses = []
    def __init__(self, user_name, user_id, email, password):
        super().__init__(user_name, user_id, email, password)


    def facilitators_list(cls):
        return cls.facilitators

    def create_facilitator(cls, user_name, user_id, email, password, course_name, course_id):
        new_facilitator = Facilitator(user_name, user_id, email, password, course_name, course_id)
        cls.facilitators.append(new_facilitator)


    def get_facilitator_size(cls):
        return len(cls.facilitators)

    def get_facilitators(cls):
        return cls.facilitators

# admin = Admin("John", "123BD", "john123@gmail.com", "0000")
# admin.create_facilitator("John", "123BD", "john123@gmail.com", "0000")
#
# print(admin.get_facilitator_size())







