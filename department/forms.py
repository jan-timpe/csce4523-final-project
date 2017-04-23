from flask_wtf import FlaskForm
from .models import Department
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length, ValidationError

class DepartmentForm(FlaskForm):
    name = StringField('Department Name', validators=[
        DataRequired(
            message="Department name is required"
        ),
        Length(
            max=50,
            message="Department name cannot be greater than 50 characters"
        )
    ])

    code = StringField('Department Code', validators=[
        DataRequired(
            message="Department code is required"
        ),
        Length(
            max=10,
            message="Department code cannot be greater than 10 characters"
        )
    ])

    # Ensure that department code is unique
    def validate_code(form, field):
        existing = Department.select().where(
            Department.code == field.data
        )
        if existing:
            raise ValidationError('Department code already in use')
