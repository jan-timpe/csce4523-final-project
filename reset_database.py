from department.models import Department
from student.models import Student, StudentEnrollment
from course.models import Course

# --- #
# Drops and recreates each table individually
# Optionally include a method to drop all database tables at once
def recreate_student_table():
    Student.drop_table(fail_silently=True)
    Student.create_table(fail_silently=True)

def recreate_department_table():
    Department.drop_table(fail_silently=True)
    Department.create_table(fail_silently=True)

def recreate_course_table():
    Course.drop_table(fail_silently=True)
    Course.create_table(fail_silently=True)

def recreate_enrollment_table():
    StudentEnrollment.drop_table(fail_silently=True)
    StudentEnrollment.create_table(fail_silently=True)
# --- #

# --- #
# Inserts two default records per table
# Call these after calling the recreate function
def seed_student_table():
    student = Student(
        email="jantimpe@email.uark.edu",
        student_id="101678608",
        first_name="Jan",
        last_name="Timpe"
    )
    student.save()

    student = Student(
        email="testtesterson@ema.il",
        student_id="74151585",
        first_name="Test",
        last_name="Testerson"
    )
    student.save()

def seed_department_table():
    dept = Department(
        name="Testing Department",
        code="TEST"
    )
    dept.save()

    dept = Department(
        name="Computer Science/Engineering",
        code="CSCE"
    )
    dept.save()

def seed_course_table():
    course = Course(
        name="Testing 101",
        number=3342,
        credit_hours=3,
        department=(Department.get(Department.id == 1))
    )
    course.save()

    course = Course(
        name="Database Management Systems",
        number=4523,
        credit_hours=3,
        department=(Department.get(Department.id == 2))
    )
    course.save()

def seed_enrollment_table():
    enrl = StudentEnrollment(
        course=(Course.get(Course.id == 1)),
        student=(Student.get(Student.id == 1))
    )
    enrl.save()

    enrl = StudentEnrollment(
        course=(Course.get(Course.id == 2)),
        student=(Student.get(Student.id == 2))
    )
    enrl.save()

# --- #

# Rebuild and seed the database
# NOTE: Do NOT use this in production, use a migration tool or migrate by hand instead
def cleanup_tables():
    recreate_student_table()
    recreate_department_table()
    recreate_course_table()
    recreate_enrollment_table()

    seed_student_table()
    seed_department_table()
    seed_course_table()
    seed_enrollment_table()
