
from managers.course_manager import CourseManager, RepeatedCourseCreationException
from models import student, instructor
from models.instructor import Instructor, CourseAlreadyCreatedException
from models.student import Student

from managers.course_manager import CourseManager
import re
from test_course_manager import InvalidEmailException


def main():
    course_manager = CourseManager()
    while True:
        print("""\nWelcome to the Student Course Management System!)
        1. Register
        2. Login as Instructor
        3. Login as Student
        4. Exit
        """)
        choice = input("\nEnter your choice! ")

        match choice:
            case "1":
                register(course_manager)
            case "2":
                login_as_instructor(course_manager)
            case "3":
                login_as_student(course_manager)
            case "4":
                print("loging out...")
                break
            case _:
                print("Invalid input!\nEnter integers from 1 to 4 only!")

def validate_id(prompt1):
    while True:
        try:
            return int(input(prompt1))
        except ValueError:
            print("Invalid Id\nId can only be entered as integer")

def validate_credit_unit(prompt2):
    while True:
        try:
            return int(input(prompt2))
        except ValueError:
            print("Invalid Credit Unit\nCredit unit can only be entered as integer")

def verify_email(email: str) -> bool:
    email_validator = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_validator, email) is not None

def register_as_instructor(course_manager):
    user_id = validate_id("Please enter your id")
    username = input("Please enter your name: ")
    password = input("Please enter your password: ")
    while True:
        email = input("Please enter your email: ")
        if verify_email(email):
            break
        print("Email is not a valid email!\nTry again!")
    instructor = Instructor(user_id, username, password, email)
    course_manager.add_instructor(instructor)
    print(f"Instructor {username} registered successfully!")


def register_as_student(course_manager):
    user_id = validate_id("Please enter your id")
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    while True:
        email = input("Please enter your email: ")
        if verify_email(email):
            break
        print("Email is not a valid email!\nTry again!")
    student = Student(user_id, username, password, email)
    course_manager.add_student(student)
    print(f"Student {username} registered successfully!")

def login_as_instructor(course_manager):
    username = input("Please enter your username: ")
    email = input("Please enter your email: ")
    password = input("Please enter your password: ")
    instructor = next((person for person in course_manager.instructors if person.username == username), None)
    if instructor:

        try:
            if not instructor.verify_email(email):
                raise InvalidEmailException("Email format is not valid!")

            if not instructor.is_email_matching(email):
                raise ValueError("OOps!\nYou have entered a wrong email!")

            if instructor.verify_password(password):
                print(f"Instructor {username} logged in successfully!")
                instructor_login(instructor, course_manager)
                return
            # if not instructor.verify_password(username):
            raise ValueError(f"Your attempt to login was unsuccessful!\nDue to an invalid username or password\nOr you may not have registered with us!")


        except InvalidEmailException as e:
            print(f"{e}")
        except ValueError as e:
            print(f"{e}")
            if str(e).startswith("Your attempt to login"):
                while True:
                    option = input(
                        "Would you like to register as an instructor?\nchoose between the option (yes/no) ").lower()
                    if option == "yes":
                        register_as_instructor(course_manager)
                        print(f"You may now login!")
                        return
                    elif option == "no":
                        return
                    else:
                        print("Invalid input!\nEnter either 'yes' or 'no'")
    else:
        print(f"Instructor not found!")

        while True:

            print(f"Your attempt to login was unsuccessful!\nDue to an invalid username or password\nOr you may not have registered with us!")
            option = input("Would you like to register as an instructor?\nchoose between the option (yes/no) ").lower()
            if option == "yes":
                register(course_manager)
                break
            elif option == "no":
                break
            else:
                print("Invalid input!\nEnter either 'yes' or 'no'")


def login_as_student(course_manager):
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    email = input("Please enter your email: ")
    student = next((person for person in course_manager.students if person.username == username), None)
    if student:

        try:
            if not student.verify_email(email):
                raise InvalidEmailException("Email format is not valid!")

            if not student.is_email_matching(email):
                raise ValueError("OOps!\nYou have entered a wrong email!")

            if student.verify_password(password):
                print(f"Instructor {username} logged in successfully!")
                student_login(course_manager)
                return
            # if not instructor.verify_password(username):
            raise ValueError(f"Your attempt to login was unsuccessful!\nDue to an invalid username or password\nOr you may not have registered with us!")

            # print(f"Instructor {username} logged in successfully!")
            # instructor_login(instructor, course_manager)
            #return
        except InvalidEmailException as e:
            print(f"{e}")
        except ValueError as e:
            print(f"{e}")
            if str(e).startswith("Your attempt to login"):
                while True:
                    option = input(
                        "Would you like to register as an instructor?\nchoose between the option (yes/no) ").lower()
                    if option == "yes":
                        register_as_student(course_manager)
                        print(f"You may now login!")
                        return
                    elif option == "no":
                        return
                    else:
                        print("Invalid input!\nEnter either 'yes' or 'no'")


    else:
        print(f"Instructor not found!")

        while True:

            print(f"Your attempt to login was unsuccessful!\nDue to an invalid username or password\nOr you may not have registered with us!")
            option = input("Would you like to register as an instructor?\nchoose between the option (yes/no) ").lower()
            if option == "yes":
                register_as_student(course_manager)
                break
            elif option == "no":
                break
            else:
                print("Invalid input!\nEnter either 'yes' or 'no'")

def instructor_login(instructor, course_manager):
    while True:
        print("""
        1. Create a course
        2. View students in a course
        3. Grade a student
        4. Logout
        """)

        choice = input("Enter your choice! ")

        match choice:
            case "1":
                create_course(instructor, course_manager)
            case "2":
                view_students_in_course(instructor, course_manager)
            case "3":
                grade_students(instructor, course_manager)
            case "4":
                print("loging out....")
                break
            case _:
                print("Invalid input!\nEnter integers from 1 and 4 only!")

def create_course(instructor, course_manager):
    course_id = validate_id("Please enter your course id")
    course_name = input("Please enter course name: ")
    credit_unit = validate_credit_unit("Please enter course credit unit: ")
    try:
        instructor.create_course(course_id, course_name, credit_unit, course_manager)
        print(f"Course {course_id} created successfully!")
    except CourseAlreadyCreatedException as e:
        print(e)
    except RepeatedCourseCreationException as e:
        print(e)

def view_students_in_course(instructor, course_manager):
    course_id = validate_id("Please enter your id")
    students = instructor.view_students(course_id, course_manager)

    # print(f"Student in course {course_id}:")
    if students and isinstance(students, list):
        for student in students:
            print(f"{student.username}: {student.username}")

    else:
        print("No student has been enrolled in your course\nYou may not have uploaded your course \non the course management portal!")

def grade_students(instructor, course_manager):


    student_id = validate_id("Please enter your student id")
    student_name = input("Please enter student name: ")
    course_id = validate_id("Please enter course id")
    grade = int(input("Please enter your student grade: "))
    result = instructor.grade_student(student_id, course_id, grade, course_manager)
    grade_category = ""
    new_grade = int(grade)

    if result:
        if 70 <= new_grade <= 100:
            grade_category = "A"
        elif 60 <= new_grade <= 69:
            grade_category = "B"
        elif 50 <= new_grade <= 59:
            grade_category = "C"
        elif 45 <= new_grade <= 49:
            grade_category = "D"
        elif 40 <= new_grade <= 44:
            grade_category = "E"
        elif new_grade <= 39:
            grade_category = "F"

        print(f"Student {student_name}: {student_id} successfully graded with score {grade}: {grade_category}!")
    else:
        print("This course has not been graded yet!")

def student_login(course_manager):
    while True:
        print("""
        1. Enroll in course
        2. View_course_instructor
        3. view_course_grade
        4. Logout
        """)

        choice = input("Enter your choice! ")
        match choice:
            case "1":
                enroll_in_a_course(course_manager)
            case "2":
                view_course_instructor(course_manager)
            case "3":
                view_course_grade(course_manager)
            case "4":
                print("Loging out...")
                break
            case _:
                print("Invalid input!\nEnter integers from 1 and 4 only!")

def enroll_in_a_course(course_manager):
    student_id = validate_id("Please enter your student id")
    course_id = validate_id("Please enter course id")
    course_name = input("Please enter course name: ")
    student = course_manager.get_student(student_id)
    course = course_manager.get_course(course_id)
    if not student:
        print("Student not found!")
        return

    if not course:
        print("Course not found!")
        return

    enrollment = course_manager.enroll_student(student_id, course_id)
    if enrollment:
        course_manager.save_to_file()
        print(f"Course {course_id} enrolled successfully!")
        return
    else:
        print("Enrollment not successful!")

    # if course:
    # # for course in courses:
    # # #     if course.course_id == course_id:
    #         print(f"You are now enrolled in {course_name}: {course_id}")
    # else:
    #         print(f"{course_name}: {course_id} does not exist\n It may not have been created\nYou may visit the portal to lay your complain!")

def view_course_instructor(course_manager):
    course_id = validate_id("Please enter course id")
    course_name = input("Please enter course name: ")
    instructor = course_manager.get_course(course_id)
    print(f"Instructor for {course_name} {course_id}: {instructor}")

def view_course_grade(course_manager):
    course_id = validate_id("Please enter course id")
    if course_manager.get_course(course_id):
        for course_id, grade in grades.items():
            print(f"Grade for {course_id}: {grade if grade else 'Grade has not been awarded yet\nOr you may not have sat for the exam!'}")

def register(course_manager):
    while True:
            choice = input("Do you want to register as an instructor or  a student\nEnter 1 for instructor or 2 for student: ")
            if choice == "1":
                register_as_instructor(course_manager)
                break
            elif choice == "2":
                register_as_student(course_manager)
                break
            else:
                print("Invalid input!\nEnter 1 aor 2 only!")

if __name__ == "__main__":
     main()