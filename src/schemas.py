from flask_marshmallow import Marshmallow

from src.config import app

ma = Marshmallow(app)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_uuid', 'username', 'user_fname',
                  'user_lname', 'user_email', 'is_user_admin',
                  'is_user_superadmin')

class BlogSchema(ma.Schema):
    class Meta:
        fields=('blog_uuid', 'blog_title', 'blog_slug', 'blog_content',
                'blog_created_at', 'blog_tags', 'blog_author_uuid',
                'blog_author_username', 'blog_author_fullname')
