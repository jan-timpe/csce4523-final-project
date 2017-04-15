from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length

class CourseForm(FlaskForm):
    name = StringField('Course Title', validators=[
        DataRequired(
            message="Course title is required"
        ),
        Length(
            max=50,
            message="Course title must be less than 50 characters"
        )
    ])
    number = IntegerField('Course Number', validators=[
        DataRequired(
            message="Course number is required"
        ),
        NumberRange(
            min=0, max=9999,
            message="Course number must be between 0 and 9999"
        )
    ])
    credit_hours = IntegerField('Credit Hours', validators=[
        DataRequired(
            message="Credit hours is required"
        ),
        NumberRange(
            min=0, max=6,
            message="Credit hours must be between 0 and 6"
        )
    ])
    department = SelectField('Department', coerce=int)
