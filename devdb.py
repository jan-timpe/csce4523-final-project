import asyncio, peewee
from peewee_async import Manager

database = peewee.SqliteDatabase('jantimpe-students-dev.db')
objects = Manager(database)
