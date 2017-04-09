from flask import abort, Blueprint, render_template, redirect, request, url_for
from .models import Course
from department.models import Department
from .forms import CourseForm

course = Blueprint('course', __name__, template_folder='templates')

def get_object_or_404(model, *args):
    try:
        return model.get(*args)
    except model.DoesNotExist:
        abort(404)

@course.route('/')
def list():
    courses = Course.select()

    return render_template(
        'course/list.html',
        title="Courses",
        courses=courses
    )

@course.route('/<department_code>/<course_number>')
def get(department_code, course_number):
    try:
        course = Course.select().join(Department).where(Department.code == department_code, Course.number == course_number).get()
    except model.DoesNotExist:
        abort(404)

    return render_template(
        'course/details.html',
        title=course.name,
        course=course
    )

@course.route('/create', methods=['GET', 'POST'])
def create():
    form = CourseForm()
    form.department.choices = [(d.id, d.name) for d in Department.select()]
    if form.validate_on_submit():
        course = Course()
        form.populate_obj(course)
        course.save()

        return redirect(course.absolute_url())

    return render_template(
        'course/form.html',
        title="Add new course",
        form=form
    )
