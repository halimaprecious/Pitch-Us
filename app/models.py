from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(150),unique = True)
    username = db.Column(db.String(150),unique = True)
    password = db.Column(db.String(150),nullable = False)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    date_created = db.Column(db.DateTime(timezone=True),default=func.now())
    pitches = db.relationship('Pitch',backref='user',passive_deletes=True)
    comments = db.relationship('Comment',backref='user',passive_deletes=True)
    likes = db.relationship('Like',backref='user',passive_deletes=True)

# class Pitch(db.Model):
#     id = db.Column(db.Integer,primary_key = True)
#     text = db.Column(db.Text,nullable=False)
#     category = db.Column(db.String, nullable=False)
#     date_created = db.Column(db.DateTime(timezone=True),default=func.now())
#     author = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
#     comments = db.relationship('Comment',backref='pitch',passive_deletes=True)
#     likes = db.relationship('Like',backref='pitch',passive_deletes=True)


# class Comment(db.Model):
#     id = db.Column(db.Integer,primary_key = True)
#     text = db.Column(db.String(200),nullable=False)
#     date_created = db.Column(db.DateTime(timezone=True),default=func.now())
#     author = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
#     pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id',ondelete='CASCADE'),nullable=False)

# class Like(db.Model):
#     id = db.Column(db.Integer,primary_key = True)
#     author = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
#     pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id',ondelete='CASCADE'),nullable=False)

