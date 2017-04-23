from flask import abort, Blueprint, render_template, redirect, request, url_for
from course.models import Course
from department.models import Department
from .forms import StudentForm
from .models import Student, StudentEnrollment
from playhouse.shortcuts import cast

# Create the module blueprint
# This is imported in main.py
student = Blueprint('student', __name__, template_folder='templates')

# a helper method
# TODO: this is repeated in every module, move to a helper functions file
def get_object_or_404(model, *args):
    try:
        return model.get(*args)
    except model.DoesNotExist:
        abort(404)


# Fetches a list of every student in the database
# Pass a url parameter [ ?q=some-search-param ] to filter results
@student.route('/')
def list():
    search_param = request.args.get('q')

    if search_param:
        students = Student.select().where(
            Student.first_name.contains(search_param)
            | Student.last_name.contains(search_param)
            | Student.email.contains(search_param)
            | Student.student_id.contains(search_param)
        ).order_by(Student.last_name.desc())
    else:
        students = Student.select().order_by(Student.last_name.desc())

    return render_template(
        'student/list.html',
        title="Students",
        students=students,
        search=search_param
    )

# Fetch a single student object by student id
# Throws a 404 error if the student is not found in the database
@student.route('/<student_id>')
def get(student_id):
    student = get_object_or_404(Student, Student.student_id == student_id)

    return render_template(
        'student/details.html',
        title=student.first_name+" "+student.last_name,
        student=student
    )

# Create a new student object
# Handles both GET and POST requests
# Redirects user to student.get() upon successful submission
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

# Edit an existing student
# Throws 404 if student lookup fails
# Redirects to student.get() on success
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

# Deletes the student
# FIXME: this allows for deleting data without confirmation through a GET request
# FIXME: add CSRF protection and DELETE request requirement
# FIXME: do this through some sort of form with confirmation
@student.route('/<student_id>/delete')
def delete(student_id):
    student = get_object_or_404(Student, Student.student_id == student_id)
    StudentEnrollment.delete().where(StudentEnrollment.student == student).execute()
    student.delete_instance()

    return redirect(url_for('student.list'))

# Retrieve a list of courses that the student is not already enrolled in
@student.route('/<student_id>/enroll', methods=['GET'])
def enroll(student_id):
    search_param = request.args.get('q')
    student = get_object_or_404(Student, Student.student_id == student_id)

    if search_param:
        courses = Course.select().join(StudentEnrollment).where(
            StudentEnrollment.student != student
            & (
                Course.name.contains(search_param)
            )
        )
    else:
        courses = Course.select().where(
            Course.id.not_in(
                StudentEnrollment.select(
                StudentEnrollment.course
            ).join(Course).where(
                    StudentEnrollment.student == student
                )
            )
        )

    return render_template(
        'student/enroll.html',
        title="Enroll",
        student=student,
        courses=courses,
        search=search_param
    )

# Handles POST requests to the student enrollment form
@student.route('/<student_id>/enroll', methods=['POST'])
def enroll_student(student_id):
    selected_courses = request.form.getlist('selected_courses')
    student = get_object_or_404(Student, Student.student_id == student_id)

    # FIXME: kill the operation if a nonexistant course id is found in the form
    # FIXME: use the database.commit() functionality here instead
    for course in Course.select().where(Course.id.in_(selected_courses)):
        enrollment = StudentEnrollment(
            student = student.id,
            course = course.id
        )
        enrollment.save()
    return redirect(student.absolute_url())

# Delete the entry from the StudentEnrollment table
# FIXME: add CSRF protection, only accept DELETE requests through a form
@student.route('/<student_id>/drop/<enrollment_id>')
def drop_course(student_id, enrollment_id):
    student = get_object_or_404(Student, Student.student_id == student_id)
    enrollment = get_object_or_404(StudentEnrollment, StudentEnrollment.id == enrollment_id)

    enrollment.delete_instance()

    return redirect(student.absolute_url())
