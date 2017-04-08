from flask import abort, Blueprint, render_template, redirect, request, url_for
from .models import Course

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
    course = get_object_or_404(Course, Course.department.code == department_code, Course.number == course_number)

    return render_template(
        'course/details.html',
        title=course.name,
        course=course
    )

# @course.route('/create', methods=['GET', 'POST'])
# def create():
