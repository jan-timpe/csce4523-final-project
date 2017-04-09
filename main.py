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
app.url_map.strict_slashes = False

app.register_blueprint(student, url_prefix='/students')
app.register_blueprint(department, url_prefix='/departments')
app.register_blueprint(course, url_prefix='/courses')

@app.before_first_request
def cleanup_tables():
    Student.create_table(fail_silently=True)
    Department.create_table(fail_silently=True)
    Course.create_table(fail_silently=True)

@app.route('/')
def home():
    return render_template('home.html', title='Welcome')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

if __name__ == "__main__":
    app.run(debug=True) # yeahh don't go into production with this.
