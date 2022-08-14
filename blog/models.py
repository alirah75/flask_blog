import datetime
from sqlalchemy.orm import relationship
from blog import db, login_manager
from sqlalchemy import Column, String, Integer, DateTime, Text
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    email = Column(String(60), unique=True, nullable=False)
    posts = relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.username})'


class Post(db.Model):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(120), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.datetime.now)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.title[:30]}, {self.date})'
