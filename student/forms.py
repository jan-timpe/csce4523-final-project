from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length

class StudentForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(max=50)
    ])

    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(max=50)
    ])

    email = StringField('Email', validators=[
        DataRequired(),
        Length(max=100),
        Email()
    ])

    student_id = StringField('Student ID', validators=[
        DataRequired(),
        Length(max=10)
    ])
