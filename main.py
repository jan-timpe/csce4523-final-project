from flask import Flask, render_template, request
from department.views import department
from department.models import Department
from student.views import student
from student.models import Student
from course.views import course
from course.models import Course
import peewee

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'

app.register_blueprint(student, url_prefix='/students')
app.register_blueprint(department, url_prefix='/departments')

@app.before_first_request
def cleanup_tables():
    Student.create_table(fail_silently=True)
    Department.create_table(fail_silently=True)
    Course.create_table(fail_silently=True)

@app.route('/')
def home():
    return render_template('home.html', title='Welcome')

if __name__ == "__main__":
    app.run()
