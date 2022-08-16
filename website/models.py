from email.policy import default
from numpy import unicode_
from . import db # . -> current package i.e website or which also means from __init__.py file import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# creating first database table/model which is user
class User(db.Model , UserMixin):
    # creating columns
    id = db.Column(db.Integer,primary_key=True) #id will be automatically generated
    email = db.Column(db.String(150),unique=True)
    username = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True),default=func.now())
    posts = db.relationship("Post",backref="user" ,passive_deletes=True)

# model that will represnt the post
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.Text,nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),default=func.now())
    author = db.Column(db.Integer , db.ForeignKey("user.id",ondelete="CASCADE"),nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),default=func.now())
    author = db.Column(db.Integer , db.ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
    post_id = db.Column(db.Integer , db.ForeignKey("post.id",ondelete="CASCADE"),nullable=False)
