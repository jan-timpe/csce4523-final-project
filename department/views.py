from flask import abort, Blueprint, render_template, redirect, request, url_for
from .models import Department
from .forms import DepartmentForm

department = Blueprint('department', __name__, template_folder='templates')

def get_object_or_404(model, *args):
    try:
        return model.get(*args)
    except model.DoesNotExist:
        abort(404)

@department.route('', strict_slashes=False)
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

@department.route('/<department_code>', strict_slashes=False)
def get(department_code):
    department = get_object_or_404(Department, Department.code == department_code)

    return render_template(
        'department/details.html',
        title=department.name,
        department=department
    )

@department.route('/create', methods=['GET', 'POST'], strict_slashes=False)
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

@department.route('/<department_code>/edit', methods=['GET', 'POST'], strict_slashes=False)
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

@department.route('/<department_code>/delete', strict_slashes=False)
def delete(department_code):
    department = get_object_or_404(Department, Department.code == department_code)
    department.delete_instance()

    return redirect(url_for('department.list'))
