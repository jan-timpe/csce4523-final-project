from flask import abort, Blueprint, render_template, redirect, request, url_for
from .models import Student, StudentEnrollment
from .forms import StudentForm
from course.models import Course
from department.models import Department
from playhouse.shortcuts import cast

student = Blueprint('student', __name__, template_folder='templates')

def get_object_or_404(model, *args):
    try:
        return model.get(*args)
    except model.DoesNotExist:
        abort(404)


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
    StudentEnrollment.delete().where(StudentEnrollment.student == student).execute()
    student.delete_instance()

    return redirect(url_for('student.list'))

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
                StudentEnrollment.select().join(Course).where(
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

@student.route('/<student_id>/enroll', methods=['POST'])
def enroll_student(student_id):
    selected_courses = request.form.getlist('selected_courses')
    print(selected_courses)

    student = get_object_or_404(Student, Student.student_id == student_id)

    # this is not a good method. slow, not ACID compliant; too many queries, potential to fail mid-query and throw an unnecessary 404

    # this is a much better method; ensures only courses that exist in the database are being added.
    for course in Course.select().where(Course.id.in_(selected_courses)):
        # course = get_object_or_404(Course, Course.id == course_id)
        print(course.name)
        print(student.full_name())
        enrollment = StudentEnrollment(
            student = student.id,
            course = course.id
        )
        enrollment.save()
    return redirect(student.absolute_url())

@student.route('/<student_id>/drop/<enrollment_id>')
def drop_course(student_id, enrollment_id):
    student = get_object_or_404(Student, Student.student_id == student_id)
    enrollment = get_object_or_404(StudentEnrollment, StudentEnrollment.id == enrollment_id)

    enrollment.delete_instance()

    return redirect(student.absolute_url())
