from database import db, objects
from department.models import Department
import peewee

class Course(peewee.Model):
    name = peewee.CharField(max_length=50)
    number = peewee.IntegerField()
    credit_hours = peewee.IntegerField()
    department = peewee.ForeignKeyField(Department, related_name='courses', on_delete='CASCADE')

    class Meta:
        database = db

    def absolute_url(self):
        return '/courses/'+self.department.code+'/'+str(self.number)
