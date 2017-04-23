from flask import abort, Blueprint, render_template, redirect, request, url_for
from .forms import CourseForm
from .models import Course
from department.models import Department
from playhouse.shortcuts import cast
from student.models import StudentEnrollment

# Create the module blueprint
course = Blueprint('course', __name__, template_folder='templates')

# TODO: repeated, move to helper functions file
def get_object_or_404(model, *args):
    try:
        return model.get(*args)
    except model.DoesNotExist:
        abort(404)

# Fetch a list of all courses
# Pass url parameter [ q=some-search ] to filter results
@course.route('/')
def list():
    search_param = request.args.get('q')

    if search_param:
        courses = Course.select().join(Department).where(
            Course.name.contains(search_param)
            | cast(Course.number, 'text').contains(search_param)
            | cast(Course.credit_hours, 'text').contains(search_param)
            | Department.name.contains(search_param)
            | Department.code.contains(search_param)
        ).order_by(Course.number)
    else:
        courses = Course.select().join(Department).order_by(Course.number)

    return render_template(
        'course/list.html',
        title="Courses",
        courses=courses,
        search=search_param
    )

# List all courses by department
# NOTE: this is not actually used anywhere and mimics the behavior of department.get() (but with added search)
# TODO: deprecate this, but keep the behavior. Make this function redirect to or present department.get()
@course.route('/<department_code>')
def list_for_department(department_code):
    # FIXME: this seems like an unneccesary first query; is there a way to get the same behavior but save a query?
    department = get_object_or_404(Department, Department.code == department_code)

    search_param = request.args.get('q')

    if search_param:
        courses = Course.select().join(Department).where(
            (Course.name.contains(search_param)
            | cast(Course.number, 'text').contains(search_param)
            | cast(Course.credit_hours, 'text').contains(search_param)
            | Department.name.contains(search_param)),
            Department.code == department_code
        ).order_by(Course.number)
    else:
        courses = Course.select().join(Department).where(Department.code == department_code)

    return render_template(
        'course/list.html',
        title=department.name+" Courses",
        courses=courses,
        search=search_param
    )

# Fetch a single course, looked up by department code and course number
# FIXME: this seriously does an unnecessary extra JOIN to make the URL look pretty.
@course.route('/<department_code>/<course_number>')
def get(department_code, course_number):
    # FIXME: definately pull this try/except out to another function; it gets reused a lot
    try:
        course = Course.select().join(Department).where(Department.code == department_code, Course.number == course_number).get()
    except model.DoesNotExist:
        abort(404)

    return render_template(
        'course/details.html',
        title=course.name,
        course=course
    )

# Create a new course object
# Redirect to course.get() upon success
@course.route('/create', methods=['GET', 'POST'])
def create():
    form = CourseForm()

    # WTForms doesn't handle relationships between objects well
    # their documentation suggests this for populating the deparment select list
    # FIXME: move this to a constructor (?) on the CourseForm object
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

# Edit a course
# Redirect to course.get() upon success
@course.route('/<department_code>/<course_number>/edit', methods=['GET', 'POST'])
def edit(department_code, course_number):
    try:
        course = Course.select().join(Department).where(Department.code == department_code, Course.number == course_number).get()
    except model.DoesNotExist:
        abort(404)

    form = CourseForm(obj=course)
    form.department.choices = [(d.id, d.name) for d in Department.select()]
    if form.validate_on_submit():
        form.populate_obj(course)
        course.save()

        return redirect(course.absolute_url())

    return render_template(
        'course/form.html',
        title="Edit course",
        form=form
    )

# Delete a course
# FIXME: add CSRF protection and require DELETE request through a form
@course.route('/<department_code>/<course_number>/delete')
def delete(department_code, course_number):
    try:
        course = Course.select().join(Department).where(Department.code == department_code, Course.number == course_number).get()
    except model.DoesNotExist:
        abort(404)


    StudentEnrollment.delete().where(StudentEnrollment.course == course).execute()
    course.delete_instance()

    return redirect(url_for('course.list'))
