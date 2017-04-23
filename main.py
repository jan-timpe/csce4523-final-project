from flask import Flask, render_template, request
import reset_database
from department.views import department
from student.views import student
from course.views import course
import peewee

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.url_map.strict_slashes = False

app.register_blueprint(student, url_prefix='/students')
app.register_blueprint(department, url_prefix='/departments')
app.register_blueprint(course, url_prefix='/courses')

# Rebuild and seed the database
# This is a dirty hack for handling migrations in development
# In production, use a migration tool or perform migrations by hand before deploying
@app.before_first_request
def cleanup_tables():
    if app.debug:
        reset_database.cleanup_tables()

# --- #
# Route for static pages
# These are fine to go in main
# essentially not worth the effort of giving them their own module
@app.route('/')
def home():
    return render_template('home.html', title='Welcome')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

# --- #

# Render a template on 404
# Optionally, override this in individual modules to provide more detailed errors
# or pass some arguments in to help the user identify the error
@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        'error/404.html',
        title="404"
    ), 404
