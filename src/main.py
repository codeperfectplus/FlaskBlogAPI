import jwt
import uuid
import datetime
import string
import random
from functools import wraps
from flask import request
from flask import jsonify
from flask import make_response

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from src.config import app
from src.models import UserModel, BlogModel
from src.models import db
from src.schemas import UserSchema, BlogSchema

''' create instance of schemas '''
user_schema = UserSchema()
users_schema = UserSchema(many=True)
blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'api-key' in request.headers:
            token = request.headers['api-key']

        if not token:
            return jsonify({'status': 'api-key is missing'}), 401

        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'])
            current_user = UserModel.query.filter_by(username=data['username']).first()
        except Exception:
            return jsonify({'status': 'api-key is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/', methods=['GET'])
def home():
    return jsonify({'status_code': '200 OK'})

@app.route('/user', methods=['POST'])
def create_user():
    ''' create new user in the database '''
    data = request.json
    print(data)
    user = UserModel.query.filter_by(username=data['username']).first()
    if user is None:
        new_user = UserModel(user_uuid=str(uuid.uuid4().hex),
                             username=data['username'],
                             user_password=generate_password_hash(data['password'],
                                                             method='sha256'),
                             user_fname=data['fname'], user_lname=data['lname'],
                             user_email=data['email'], is_user_admin=False,
                             is_user_superadmin=False)

        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user)

    return jsonify({'status': f'{data.username} is already a user.'})

@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.is_user_admin:
        return jsonify({'status': 'You are not admin'})
    users = UserModel.query.all()
    result = users_schema.dump(users)
    return jsonify(result)

@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify!', 401, {'WWW-Authentication': 'Basic realm=Login Required'})

    user = UserModel.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('could not verify!', 401, {'WWW-Authentication': 'Basic realm=Login Required'})

    if check_password_hash(user.user_password, auth.password):
        token = jwt.encode({'username': user.username},
                            app.config['JWT_SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('could not verify!', 401, {'WWW-Authentication': 'Basic realm=Login Required'})

''' Blogs APi routes '''
@app.route('/blog', methods=['POST'])
@token_required
def create_blog(current_user):
    data = request.json

    new_blog = BlogModel(blog_uuid=str(uuid.uuid4()), blog_title=data['blog_title'],
                         blog_slug=data['blog_title'].replace(' ', '-') + "-" + ''.join(random.choice(string.ascii_lowercase) for _ in range(4)),
                         blog_content=data['blog_content'],
                         blog_created_at=datetime.datetime.utcnow(),
                         blog_tags=data['blog_tags'],
                         blog_author_uuid=current_user.user_uuid,
                         blog_author_username=current_user.username,
                         blog_author_fullname=current_user.user_fname)
    db.session.add(new_blog)
    db.session.commit()

    return blog_schema.jsonify(new_blog)

@app.route('/blog', methods=['GET'])
def get_all_blogs():
    blogs = BlogModel.query.all()
    result = blogs_schema.dump(blogs)
    return jsonify(result)

@app.route('/<blog_author_username>', methods=['GET'])
def get_all_user_blog(blog_author_username):
    blogs = BlogModel.query.filter_by(blog_author_username=blog_author_username).all()
    print(blogs)
    result = blogs_schema.dump(blogs)
    return jsonify(result)


@app.route("/blog/<blog_uuid>", methods=['DELETE'])
@token_required
def delete_blog(current_user, blog_uuid):
    blog = BlogModel.query.filter_by(blog_author_username=current_user.username, blog_uuid=blog_uuid).first()

    print(blog)
    if blog is None:
        return jsonify({'status': "Blog doesn't exists"})
    db.session.delete(blog)
    db.session.commit()

    return jsonify({'status': 'Blog deleted'})
