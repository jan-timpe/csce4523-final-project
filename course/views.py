from flask import abort, Blueprint, render_template, redirect, request, url_for
from .models import Course

course = Blueprint('course', __name__, template_folder='templates')

def get_object_or_404(model, *args):
    try:
        return model.get(*args)
    except model.DoesNotExist:
        abort(404)

@department.route('/')
def list():
    courses = Course.select()

    return render_template(
        'course/list.html',
        title="Courses",
        courses=courses
    )
