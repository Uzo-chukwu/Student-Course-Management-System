from managers import course_manager
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
        print("="*80)
        print("""\nWelcome to the Student Course Management System🚶‍🚶‍♂️🚶‍♂️!
        
        1. Register
        2. Login as Instructor
        3. Login as Student
        4. Exit
        """)
        print("=" * 80)
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
                print("=" * 80)
                print("""
                        OOps🙍!
                        Invalid choice. choice's can only be entered as integers from 1 to 4
                        
                        """)

def validate_id(prompt1):
    while True:
        try:
            return int(input(prompt1))
        except ValueError:
            print("="*80)
            print("""
            OOps🙍!
            Invalid Id. Id's can only be entered as integer""")

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
    print("="*80)
    print("""
        Registering as Instructor...
    """)
    print("=" * 80)
    user_id = validate_id("Please enter your id")
    username = input("Please enter your name: ")
    password = input("Please enter your password: ")
    while True:
        email = input("Please enter your email: ")
        if not verify_email(email):

            print("=" * 80)
            print("""
                                OOps🙍!
                                Email is not valid!
                                Try again!

                                """)
            continue
        if course_manager.is_email_taken(email):
            print("=" * 80)
            print("""
                                            OOps🙍!
                                            Email already exists!
                                            provide another email!

                                            """)
            continue
        break


    instructor = Instructor(user_id, username, password, email)
    course_manager.add_instructor(instructor)
    print("=" * 80)
    print(f"Instructor {username} registered successfully!")
    print(f"We are thrilled to have you in our Institution 🤝🤝!")


def register_as_student(course_manager):
    print("=" * 80)
    print("""
            Registering as Student...
        """)
    print("=" * 80)
    user_id = validate_id("Please enter your id")
    username = input("Please enter your name: ")
    password = input("Please enter your password: ")
    while True:
        email = input("Please enter your email: ")
        if not verify_email(email):
            print("=" * 80)
            print("""
                                    OOps🙍!
                                    Email is not valid!
                                    Try again!

                                    """)
            continue
        if course_manager.is_email_taken(email):
            print("=" * 80)
            print("""
                                                OOps🙍!
                                                Email already exists!
                                                provide a another email!

                                                """)
            continue
        break

    student = Student(user_id, username, password, email)
    course_manager.add_student(student)
    print("="*80)
    print(f"Student {username} registered successfully!")
    print(f"We are thrilled to have you in our Institution 🤝🤝!")


def login_as_instructor(course_manager):
    print("=" * 80)
    print("""
            Login in as Student...
        """)
    print("=" * 80)
    username = input("Please enter your username: ")
    email = input("Please enter your email: ")
    password = input("Please enter your password: ")

    print("="*80)
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
            print("="*80)
            raise ValueError ("Your attempt to login was unsuccessful!\n\nDue to an invalid username or password \n\nYou may not have registered with us!")


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

                        print("=" * 80)
                        print("""
                                                        OOps🙍!
                                                        Invalid input!
                                                        Enter either 'yes' or 'no'!

                        """)

                        print("="*80)

    else:
        print(f"Instructor not found!")

        while True:

            print("=" * 80)
            print("""
            Your attempt to login was not successful!
            Due to an invalid username or password 
            You may not have registered with us!
            """)
            option = input("Would you like to register as an instructor?\nchoose between the option (yes/no) ").lower()
            if option == "yes":
                register(course_manager)
                break
            elif option == "no":
                break
            else:
                print("=" * 80)
                print("""
                                                                        OOps🙍!
                                                                        Invalid input!
                                                                        Enter either 'yes' or 'no'!

                                        """)

                print("=" * 80)


def login_as_student(course_manager):
    print("="*80)
    print("Logging in Student...")
    print("="*80)
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
                print(f"Student {username} logged in successfully!")
                student_login(course_manager)
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
                        register_as_student(course_manager)
                        print(f"You may now login!")
                        return
                    elif option == "no":
                        return
                    else:
                        print("=" * 80)
                        print("""
                                                                                OOps🙍!
                                                                                Invalid input!
                                                                                Enter either 'yes' or 'no'!

                                                """)

                        print("=" * 80)


    else:
        print(f"Instructor not found!")

        while True:

            print("""
            Your attempt to login was unsuccessful!
            Due to an invalid username or password
            You may not have registered with us!
            """)
            print("=" * 80)
            option = input("Would you like to register as an instructor?\nchoose between the option (yes/no) ").lower()
            if option == "yes":
                register_as_student(course_manager)
                break
            elif option == "no":
                break
            else:
                print("=" * 80)
                print("""
                                                                        OOps🙍!
                                                                        Invalid input!
                                                                        Enter either 'yes' or 'no'!

                                        """)

                print("=" * 80)

def instructor_login(instructor, course_manager):
    print("="*80)
    print("""
    
        Instructors DashBoard...
    """)
    print("="*80)
    while True:
        print("""
        1. Create a course
        2. View students in a course
        3. Grade a student
        4. View student performance chart
        5. Overall Best Student
        6. Overall Worst student
        7. Logout
        """)

        choice = input("Enter your choice! ")

        match choice:
            case "1":
                create_course(instructor, course_manager)
            case "2":
                view_students_in_course(instructor, course_manager)
            case "3":
                grade_students(instructor, course_manager)
            case "5":
                overall_best_student(course_manager)
            case "4":
                get_performance_chart(course_manager)
            case "6":
                overall_worst_student(course_manager)
            case "7":
                print("loging out....")
                break
            case _:
                print("Invalid input!\nEnter integers from 1 and 4 only!")
    print("="*80)

def create_course(instructor, course_manager):
    print("="*150)
    print("\t\tWelcome to the Academic Hub 👨‍🎓👨‍🎓!")
    print("\t\tWe are concerned about your Excellence")
    print("="*80)
    course_id = validate_id("Please enter your course id")
    course_name = input("Please enter course name: ")
    credit_unit = validate_credit_unit("Please enter course credit unit: ")
    try:
        instructor.create_course(course_id, course_name, credit_unit, course_manager)
        print(f"{course_name}: {course_id} created successfully!")
    except CourseAlreadyCreatedException as e:
        print(e)
    except RepeatedCourseCreationException as e:
        print(e)

def view_students_in_course(instructor, course_manager):
    print("="*80)
    print("Viewing students in course...")
    course_id = validate_id("Please enter your id")
    students = instructor.view_students(course_id, course_manager)

    if students and isinstance(students, list):
        print(f"The students offering your course are:")
        for student in students:

            print(f"{student.username}")

    else:

        print("=" * 80)
        print("""
                                                            OOps🙍!
                                                            No student has been enrolled in your course
                                                            You may not have uploaded your course
                                                            on the course management portal!"
                                                                            

        """)

        print("=" * 80)



def grade_students(instructor, course_manager):
    print("="*80)
    print("""
    
    Welcome to the Exams and Record Department...
    📚📚
    """)
    print("="*80)
    student_id = validate_id("Please enter your student id")
    student_name = input("Please enter student name: ")
    course_id = validate_id("Please enter course id")

    try:
        grade = int(input("Please enter your student grade: "))

    except ValueError:
        print(f"Invalid value.\nEnter an integer from 0 to 100")
        return

    if not 0 <= grade <= 100:
        print(f"Enter an integer from 0 to 100!")
        return
    success, result = instructor.grade_student(student_id, course_id, grade, course_manager)
    grade_category = ""

    if success:
        if 70 <= grade <= 100:
            grade_category = "A"
        elif 60 <= grade <= 69:
            grade_category = "B"
        elif 50 <= grade <= 59:
            grade_category = "C"
        elif 45 <= grade <= 49:
            grade_category = "D"
        elif 40 <= grade <= 44:
            grade_category = "E"
        elif grade <= 39:
            grade_category = "F"

        print(f"Student {student_name}: {student_id} successfully graded with score {grade}: {grade_category}!")
    else:
        print(result)


def view_enrolled_courses(course_manager):
    student_name = input("Please enter student name: ")
    student_id = validate_id("Please enter your student id")
    student = course_manager.get_student(student_id)
    if not student:
        print(f"Student with ID: {student_id}  profile does not exist in this institution")
        return
    enrolled_courses = student.get_all_enrolled_courses(course_manager)

    if not enrolled_courses:
        print(f"You have not enrolled any course in this institution\nVisit the school portal to enroll")
        return
    print(f"Dear {student_name}: {student_id},You have enrolled for {len(enrolled_courses)} courses\n The courses are:")
    for course_detials in enrolled_courses:
        print(f"Name: {course_detials.name}, ID: {course_detials.course_id}, credits: {course_detials.credits}")


def student_login(course_manager):
    print("="*80)
    print("Welcome to Student Department...")
    while True:
        print("""
        1. Enroll in course
        2. View_course_instructor
        3. view_course_grade
<<<<<<< HEAD
        4. view_list_of_offered_courses
=======
        4. View enrolled courses
>>>>>>> fea5b31 (student course new version)
        5. Logout
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
<<<<<<< HEAD
                view_list_of_offered_courses(course_manager)
=======
                view_enrolled_courses(course_manager)
>>>>>>> fea5b31 (student course new version)
            case "5":
                print("Loging out...")
                break
            case _:
                print("Invalid input!\nEnter integers from 1 and 4 only!")

    print("="*80)

def enroll_in_a_course(course_manager):
    print("="*80)
    print("""
        Welcome to the Course Portal Department...
        Ensure you register courses that are inline with your field!
    """)
    print("="*80)
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
        print(f"{course_name} {course_id} enrolled successfully!")
        return
    else:
        print("Enrollment not successful!")

def view_course_instructor(course_manager):
    print("="*80)
    print("""
            Welcome to the Instructors Portal... 🧑‍🏫🧑‍🏫
    """)
    print("="*80)

    course_id = validate_id("Please enter course id")
    course_name = input("Please enter course name: ")
    course = course_manager.get_course(course_id)
    if not course:
        print("Course not found!\nIt may not have been created yet!")
        return
    instructor = course.instructor
    if not instructor:
        print(f"Instructor has not been assigned to this {course_name}: {course_id}!")
        return

    print(f" (ID: {course_name}: {course_id}) is {instructor}.)")

def view_course_grade(course_manager):
    print("="*80)
    print("""
    
    Welcome to the Exams and Records Department...
    📚📚
    """)
    print("="*80)
    student_id = validate_id("Please enter your student id")
    course_id = validate_id("Please enter course id")
<<<<<<< HEAD
    if course_manager.get_course(course_id):
        for course_id, grade in grades.items():
            print(f"Grade for {course_id}: {grade if grade else 'Grade has not been awarded yet. Or you may not have sat for the exam!'}")

def view_list_of_offered_courses(course_manager):
    course_id = validate_id("Please enter course ID")
    course = course_manager.get_course(course_id)
    if course is None:
        print(f"Course {course_id} is not among the list of courses you enrolled in!")
    else:
        print(course)
=======

    student = course_manager.get_student(student_id)
    if not student:
        print("Student not found!")
        return

    if not student.enrolled_courses:
        print(f"You have not enrolled in any course yet!\nDo you want to enroll in course?")
        while True:
            student_choice = input("yes or no? : ").lower()
            if student_choice == "yes":
                enroll_in_a_course(course_manager)
                return
            elif student_choice == "no":
                return
            else:
                print("Invalid input!\nEnter yes or no!")
    for course_id, grade in student.enrolled_courses.items():
        if grade is not None:
            print(f"Grade for {course_id} is: {grade}")

        else:
            print(f"Course {course_id} has not been graded yet!\nYou may not have sat for the exam!\nVisit your instructor for further complains!")


def overall_best_student(course_manager):

    course_id = validate_id("Enter course Id: ")

    instructor = course_manager.get_instructor(course_id)
    if not instructor:
        print("You ar not the tutor of this course!")
        return
    print(instructor.best_student(course_id, course_manager))

def overall_worst_student(course_manager):
    instructor_id = validate_id("Enter your id")
    instructor = course_manager.get_instructor(instructor_id)

    if not instructor:
        print("Instructor not found")
        return

    course_id = validate_id("Enter course Id: ")
    print(instructor.worst_student(course_id, course_manager))


def get_performance_chart(course_manager):
    instructor_id = validate_id("Enter your ID: ")
    course_id = validate_id("Enter your course_id: ")
    course_name = input("Enter course name: ")
    instructor = next((person for person in course_manager.instructors if  person.user_id == instructor_id), None)

    if instructor:
        print("=" * 80)
        print(f"Performance chart for {course_name}: {course_id}")
        print("=" * 80)
        print(instructor.get_students_performance_chart(course_manager))
        print("=" * 80)

    else:
        print("Instructor cannot be found!")



>>>>>>> fea5b31 (student course new version)

def register(course_manager):
    print("="*80)
    print("""
    
        Welcome to Lagbaja Tertiary Institution Portal...🚶‍🚶‍♂️🚶‍
    
    """)
    print("="*80)
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
