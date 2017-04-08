from database import db, objects
import peewee

class Department(peewee.Model):
    name = peewee.CharField(max_length=50)
    code = peewee.CharField(max_length=10, unique=True)

    class Meta:
        database = db

    def absolute_url(self):
        return '/departments/'+self.code
