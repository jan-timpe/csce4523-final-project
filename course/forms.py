from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length

class CourseForm(FlaskForm):
    name = StringField('Course Title', validators=[
        DataRequired(),
        Length(max=50)
    ])
    number = IntegerField('Course Number', validators=[
        DataRequired(),
        NumberRange(min=1000, max=9999)
    ])
    credit_hours = IntegerField('Credit Hours', validators=[
        DataRequired(),
        NumberRange(min=0, max=6)
    ])
    department = SelectField('Department', coerce=int)
