from flask import Flask, render_template, request
from student.views import student
from student.models import Student
import peewee

app = Flask(__name__)
app.register_blueprint(student, url_prefix='/students')

@app.before_first_request
def cleanup_tables():
    Student.drop_table(fail_silently=True)
    Student.create_table(fail_silently=True)

    s = Student(
        email="jantimpe@email.uark.edu",
        student_id = "01001101",
        first_name="Jan",
        last_name="Timpe"
    )
    s.save()

@app.route('/')
def home():
    return render_template('home.html', title='Welcome')

if __name__ == "__main__":
    app.run()
