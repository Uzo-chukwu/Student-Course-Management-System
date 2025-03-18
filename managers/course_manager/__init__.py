from managers import course_manager
from models.student import Student
from models.instructor import Instructor
from models.course import Course
from models.enrollment import Enrollment

class RepeatedCourseCreationException(Exception):
    pass


class CourseManager:
    def __init__(self):
        self.students = []
        self.instructors = []
        self.courses = []
        self.enrollments = []
        self.load_from_file()

    def add_student(self, student: Student):
        self.students.append(student)
        self.save_to_file()

    def add_instructor(self, instructor: Instructor):
        from test_course_manager import InvalidEmailException
        if not instructor.verify_email(instructor.email):
            raise InvalidEmailException("Invalid email format!")

        for person in self.instructors:
            if person.email == instructor.email:
                # print("Instructor already exists!")
                return person
        self.instructors.append(instructor)
        self.save_to_file()

    def add_course(self, course: Course):
        if any(specific_course.course_id == course.course_id for specific_course in self.courses):

                raise RepeatedCourseCreationException("Course already exists!")
        self.courses.append(course)
        self.save_to_file()

    def enroll_student(self, student_id: int, course_id: int):
        for enrollment in self.enrollments:
            if enrollment.student_id == student_id and enrollment.course_id == course_id:
                print(f"student {student_id} enrolled has already been enrolled in {course_id}")
                return None


        enrollment = Enrollment(len(self.enrollments) + 1, student_id, course_id)
        self.enrollments.append(enrollment)
        student = self.get_student(student_id)
        if student:
            student.enroll_course(course_id)
        else:
            print(f"student {student_id} not found!")
            return None
        self.save_to_file()
        return enrollment

    def get_student(self, student_id: int):
        for student in self.students:
            if student.user_id == student_id:
                return student
        return None

    def get_course(self, course_id: int):
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None

    def get_students_in_course(self, course_id: int):
        students = []
        for enrollment in self.enrollments:
            if enrollment.course_id == course_id:
                student = self.get_student(enrollment.student_id)
                if student:
                    students.append(student)

        return students

    def get_instructor(self, course_id: int):
        for instructor in self.instructors:  # Iterate over the list
            if course_id in instructor.taught_courses:  # Check if instructor teaches this course
                return instructor
        return None
    @property
    def get_size_of_students(self):
        return len(self.students)

    @property
    def get_size_of_instructor(self):
        return len(self.instructors)

    @property
    def get_size_of_course(self):
        return len(self.courses)

    def get_all_created_courses(self):
        return self.courses

    def is_email_taken(self, email):
        return any(student.email == email for student in self.students) or any(instructor.email == email for instructor in self.instructors)


    def save_to_file(self):
            with open('students.txt', 'w') as f:
                f.write('Students:\n')
                for student in self.students:
                    f.write(f"{student.user_id},{student.username},{student.password.decode('utf-8')},{student.email}\n")
            with open('instructors.txt', 'w') as u:
                u.write('Instructors:\n')
                for instructor in self.instructors:
                    u.write(f"{instructor.user_id},{instructor.username},{instructor.password.decode('utf-8')},{instructor.email}\n")
            with open('courses.txt', 'w') as b:
                 b.write('Courses:\n')
                 for course in self.courses:
                     b.write(f"{course.course_id},{course.name},{course.credits}\n")

            with open('enrollments.txt', 'w') as v:
                v.write('Enrollments:\n')
                for enrollment in self.enrollments:
                    v.write(f"{enrollment.enrollment_id},{enrollment.student_id},{enrollment.course_id}\n")
    def load_from_file(self):
        try:

            with open('students.txt', 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith("Students:"):
                        try:
                            user_id, username, password_hash, email = line.strip().split(',')
                            password_hash = password_hash.encode('utf-8')
                            self.students.append(Student(int(user_id), username, password_hash, email))
                        except ValueError:
                            print(f"Error reading student data: {line}")

            with open('instructors.txt', 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith("Instructors:"):
                        try:
                            user_id, username, password_hash, email = line.strip().split(',')
                            password_hash = password_hash.encode('utf-8')
                            self.instructors.append(Instructor(int(user_id), username, password_hash, email))
                        except ValueError:
                            print(f"Error reading instructor data: {line}")

            with open('courses.txt', 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith("Courses:"):
                        try:
                            course_id, name, credits = line.strip().split(',')
                            self.courses.append(Course(int(course_id), name, Instructor,  int(credits)))
                        except ValueError:
                            print(f"Error reading course data: {line}")


            with open('enrollments.txt', 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith("Enrollments:"):
                        try:
                            enrollment_id, student_id, course_id = line.strip().split(',')
                            self.enrollments.append(Enrollment(int(enrollment_id), int(student_id), int(course_id)))
                        except ValueError:
                            print(f"Error reading enrollment data: {line}")

        except FileNotFoundError:
            print("No previous data found, starting fresh.")


if __name__ == "__main__":

    manager = CourseManager()

    print(manager.get_course(course_id=404))
