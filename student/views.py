from flask import abort, Blueprint, render_template, redirect, request, url_for
from .models import Student
from .forms import StudentForm

student = Blueprint('student', __name__, template_folder='templates')

def get_object_or_404(model, *args):
    try:
        return model.get(*args)
    except model.DoesNotExist:
        abort(404)


@student.route('/')
def list():
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

@student.route('/create', methods=['GET', 'POST'])
def create():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student()
        form.populate_obj(student)
        student.save()

        return redirect(student.absolute_url())

    return render_template(
        'student/form.html',
        title="Add a new student",
        form=form
    )

@student.route('/<student_id>/edit', methods=['GET', 'POST'])
def edit(student_id):
    student = get_object_or_404(Student, Student.student_id == student_id)
    form  = StudentForm(obj=student)
    if form.validate_on_submit():
        form.populate_obj(student)
        student.save()

        return redirect(student.absolute_url())

    return render_template(
        'student/form.html',
        title="Edit student",
        form=form
    )

@student.route('/<student_id>/delete')
def delete(student_id):
    student = get_object_or_404(Student, Student.student_id == student_id)
    student.delete_instance()

    return redirect(url_for('student.list'))
