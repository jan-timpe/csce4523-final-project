from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from .models import Student

class StudentForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(
            message="First name is required"
        ),
        Length(
            max=50,
            message="First name cannot be longer than 50 characters"
        )
    ])

    last_name = StringField('Last Name', validators=[
        DataRequired(
            message="Last name is required"
        ),
        Length(
            max=50,
            message="Last name cannot be longer than 50 characters"
        )
    ])

    email = StringField('Email', validators=[
        DataRequired(
            message="Email is required"
        ),
        Length(
            max=100,
            message="Email cannot be longer than 50 characters"
        ),
        Email(
            message="Must be an email address"
        )
    ])

    student_id = StringField('Student ID', validators=[
        DataRequired(
            message="Student ID is required"
        ),
        Length(
            max=10,
            message="Student ID cannot be longer than 10 characters"
        )
    ])

    def validate_student_id(form, field):
        existing = Student.select().where(
            Student.student_id == field.data
        )
        if existing:
            raise ValidationError('Student ID already in use')

    def validate_email(form, field):
        existing = Student.select().where(
            Student.email == field.data
        )
        if existing:
            raise ValidationError('Email already in use')
