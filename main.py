from flask import Flask, render_template, request
from department.views import department
from department.models import Department
from student.views import student
from student.models import Student, StudentEnrollment
from course.views import course
from course.models import Course
import peewee

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.url_map.strict_slashes = False

app.register_blueprint(student, url_prefix='/students')
app.register_blueprint(department, url_prefix='/departments')
app.register_blueprint(course, url_prefix='/courses')

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

# Rebuild and seed the database
# This is a dirty hack for handling migrations in development
# In production, use a migration tool or perform migrations by hand before deploying
@app.before_first_request
def cleanup_tables():
    if app.debug:
        recreate_student_table()
        recreate_department_table()
        recreate_course_table()
        recreate_enrollment_table()

        seed_student_table()
        seed_department_table()
        seed_course_table()
        seed_enrollment_table()

# --- #
# Route for static pages
# These are fine to go in main
# essentially not worth the effort of giving them their own module
@app.route('/')
def home():
    return render_template('home.html', title='Welcome')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

# --- #

# Render a template on 404
# Optionally, override this in individual modules to provide more detailed errors
# or pass some arguments in to help the user identify the error
@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        'error/404.html',
        title="404"
    ), 404
