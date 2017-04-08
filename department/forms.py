from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length

class DepartmentForm(FlaskForm):
    name = StringField('Department Name', validators=[
        DataRequired(),
        Length(max=50)
    ])

    code = StringField('Department Code', validators=[
        DataRequired(),
        Length(max=10)
    ])
