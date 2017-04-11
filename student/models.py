from database import db, objects
import peewee
from course.models import Course

class Student(peewee.Model):
    email = peewee.CharField(max_length=100, unique=True)
    student_id = peewee.CharField(max_length=10, unique=True)
    first_name = peewee.CharField(max_length=50)
    last_name = peewee.CharField(max_length=50)

    class Meta:
        database = db

    def absolute_url(self):
        return '/students/'+self.student_id

    def full_name(self):
        return self.first_name+" "+self.last_name

class StudentEnrollment(peewee.Model):
    course = peewee.ForeignKeyField(Course, related_name="enrolled_students")
    student = peewee.ForeignKeyField(Student, related_name="courses")

    class Meta:
        database = db
