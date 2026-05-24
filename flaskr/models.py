from datetime import datetime
from flaskr.database import database
from sqlalchemy import (
    Column, ForeignKey, Integer, DateTime, String, Text
)


class User(database.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Post(database.Model):
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('user.id'))
    created = Column(DateTime, default=datetime.now)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)

    author = database.relationship(User, backref='post', uselist=False)

    def __repr__(self):
        return f'<Post {self.title}>'
