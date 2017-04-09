from database import db, objects
import peewee
from department.models import Department

class Course(peewee.Model):
    name = peewee.CharField(max_length=50)
    number = peewee.IntegerField()
    credit_hours = peewee.IntegerField()
    department = peewee.ForeignKeyField(Department, related_name='courses')

    class Meta:
        database = db

    def absolute_url(self):
        return '/courses/'+self.department.code+'/'+str(self.number)
