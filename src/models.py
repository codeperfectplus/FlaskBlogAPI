import datetime
from flask_sqlalchemy import SQLAlchemy

from src.config import app

db = SQLAlchemy(app)

class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    user_password = db.Column(db.String(50), nullable=False)
    user_fname = db.Column(db.String(30), nullable=False)
    user_lname = db.Column(db.String(30), nullable=False)
    user_email = db.Column(db.String(30), nullable=False)
    is_user_admin = db.Column(db.Boolean)
    is_user_superadmin = db.Column(db.Boolean)


    def __init__(self, user_uuid, username, user_password, user_fname,
                 user_lname, user_email, is_user_admin, is_user_superadmin):

        self.user_uuid = user_uuid
        self.username = username
        self.user_password = user_password
        self.user_fname = user_fname
        self.user_lname = user_lname
        self.user_email = user_email
        self.is_user_admin = is_user_admin
        self.is_user_superadmin = is_user_superadmin

    def __repr__(self):
        return self.username

class BlogModel(db.Model):
    __tablename__ = 'blogs'

    blog_id = db.Column(db.Integer, primary_key=True)
    blog_uuid = db.Column(db.String(50), nullable=False, unique=True)
    blog_title = db.Column(db.String(80), nullable=False)
    blog_slug = db.Column(db.String(100), nullable=False, unique=True)
    blog_content = db.Column(db.Text, nullable=False)
    blog_created_at = db.Column(db.String(40))
    blog_tags = db.Column(db.String(30), nullable=True)
    blog_author_uuid = db.Column(db.String(50), nullable=False)
    blog_author_username = db.Column(db.String(30), nullable=False)
    blog_author_fullname = db.Column(db.String(60), nullable=False)


    def __init__(self, blog_uuid, blog_title, blog_slug, blog_content,
                 blog_created_at, blog_tags, blog_author_uuid,
                 blog_author_username, blog_author_fullname):

        self.blog_uuid = blog_uuid
        self.blog_title = blog_title
        self.blog_slug = blog_slug
        self.blog_content = blog_content
        self.blog_created_at = blog_created_at
        self.blog_tags = blog_tags
        self.blog_author_uuid = blog_author_uuid
        self.blog_author_username = blog_author_username
        self.blog_author_fullname = blog_author_fullname


    def __repr__(self):
        return self.blog_title
