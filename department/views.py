from flask import abort, Blueprint, redirect, render_template, request, url_for
from .forms import DepartmentForm
from .models import Department

# Create the module blueprint
department = Blueprint('department', __name__, template_folder='templates')

# TODO: repeated, move to helper functions file
def get_object_or_404(model, *args):
    try:
        return model.get(*args)
    except model.DoesNotExist:
        abort(404)

# Fetch a list of all departments
# Pass a url parameter [ ?q=some-search ] to filter results
@department.route('/')
def list():
    search_param = request.args.get('q')

    if search_param:
        departments = Department.select().where(
            Department.name.contains(search_param)
            | Department.code.contains(search_param)
        ).order_by(Department.name.desc())
    else:
        departments = Department.select().order_by(Department.name.desc())

    return render_template(
        'department/list.html',
        title="Departments",
        departments=departments,
        search=search_param
    )

# Fetch a single department object by department code
# Throws 404 if lookup fails
@department.route('/<department_code>')
def get(department_code):
    department = get_object_or_404(Department, Department.code == department_code)

    return render_template(
        'department/details.html',
        title=department.name,
        department=department
    )

# Create a new department object
# Redirects to department.get() after submission
@department.route('/create', methods=['GET', 'POST'])
def create():
    form = DepartmentForm()

    if form.validate_on_submit():
        department = Department()
        form.populate_obj(department)
        department.save()

        return redirect(department.absolute_url())

    return render_template(
        'department/form.html',
        title="Add new department",
        form=form
    )

# Edit the department object
# Redirect to department.get() after submission
@department.route('/<department_code>/edit', methods=['GET', 'POST'])
def edit(department_code):
    department = get_object_or_404(Department, Department.code == department_code)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        form.populate_obj(department)
        department.save()

        return redirect(department.absolute_url())

    return render_template(
        'department/form.html',
        title="Edit department",
        form=form
    )

# Delete a department object
# FIXME: add CSRF protection and require DELETE requests through a form
@department.route('/<department_code>/delete')
def delete(department_code):
    department = get_object_or_404(Department, Department.code == department_code)
    department.delete_instance()

    return redirect(url_for('department.list'))
