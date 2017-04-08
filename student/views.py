from flask import Blueprint, render_template, request, abort
from .models import Student

student = Blueprint('student', __name__, template_folder='templates')

def get_object_or_404(model, *args):
    try:
        return model.get(*args)
    except model.DoesNotExist:
        abort(404)


@student.route('/')
def home():
    students = Student.select()

    return render_template(
        'student/list.html',
        title="Students",
        students=students
    )

@student.route('/<student_id>')
def get(student_id):
    student = get_object_or_404(Student, Student.student_id == student_id)
    return render_template(
        'student/details.html',
        title=student.first_name+" "+student.last_name,
        student=student
    )

@student.route('/create')
def create():
