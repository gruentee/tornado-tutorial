"""Application database models"""

from peewee import *
import datetime

db = SqliteDatabase('blog.db')

class Author(Model):
    """Model representing a single post author"""
    name = CharField()
    email = CharField()
    picture = CharField()

    class Meta:
        database = db

class Post(Model):
    """Model representing a single blog post"""
    title = CharField()
    slug = CharField(unique=True)
    author = ForeignKeyField(Author, related_name='posts')
    text = TextField()
    date_created = DateTimeField(default=datetime.datetime.now, index=True)
    # TODO: tags, category

    class Meta:
        database = db


