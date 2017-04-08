from database import db, objects
import peewee

class Student(peewee.Model):
    email = peewee.CharField(max_length=100, unique=True)
    student_id = peewee.CharField(max_length=10, unique=True)
    first_name = peewee.CharField(max_length=50)
    last_name = peewee.CharField(max_length=50)

    class Meta:
        database = db
