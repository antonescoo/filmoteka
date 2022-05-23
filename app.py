import os.path

from flask import Flask, jsonify, url_for, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from markupsafe import Markup

from config import Configuration
from werkzeug.security import generate_password_hash

from flask_migrate import Migrate

from flask_admin import Admin, form
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

from flask_security import SQLAlchemyUserDatastore, Security, current_user

app = Flask(__name__)
app.config.from_object(Configuration)

file_path = os.path.abspath(os.path.dirname(__name__))

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import *


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class AdminView(AdminMixin, ModelView):
    pass


class FilmsView(AdminMixin, ModelView):
    form_extra_fields = fields = {
        'poster': form.ImageUploadField(label='Poster', base_path=os.path.join(
            file_path,
            'static/images/'),
                                        url_relative_path='images/',
                                        allowed_extensions=['jpg', 'jpeg', 'png'],
                                        max_size=(1200, 780, True),
                                        thumbnail_size=(100, 100, True))
    }

    def _list_thumbnail(view, context, model, name):
        if not model.poster:
            return ''
        model.poster_thumb = model.poster.split('.')[0] + '_thumb.' + \
                        model.poster.split('.')[-1]
        url = url_for('static', filename=os.path.join('images', model.poster_thumb))
        if model.poster_thumb.split('.')[-1] in ['jpg', 'jpeg', 'png', 'svg', 'gif']:
            return Markup(f'<img src={url} width="100px">')

    column_formatters = {
        'poster': _list_thumbnail
    }


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


admin = Admin(app, 'Filmoteka', url='/films', index_view=HomeAdminView(
    name='Home'))
admin.add_view(FilmsView(Films, db.session))
admin.add_view(AdminView(Genres, db.session))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# db.create_all()

client = app.test_client()

tutorials = [
    {
        'id': 1,
        'title': 'Video #1, Intro',
        'description': 'PUT, DELETE routes'
    },
    {
        'id': 2,
        'title': 'Video #2, More features',
        'description': 'PUT, DELETE routes'
    }
]


@app.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        try:
            hash = generate_password_hash(request.form['psw'])
            u = 12
            db.session.add(u)
            db.session.flush()

            db.session.commit()
        except:
            db.session.rollback()
            print('Error adding to DB')

    return render_template('register.html', title='Регистрация')


def get_list():
    return jsonify(tutorials)


@app.route('/tutorials', methods=['POST'])
def update_list():
    new_one = request.json
    tutorials.append(new_one)
    return jsonify(tutorials)


@app.route('/genres', methods=['GET'])
def genres():
    return jsonify(tutorials)


@app.route('/tutorials/<int:tutorial_id>', methods=['PUT'])
def update_tutorial(tutorial_id):
    item = next((x for x in tutorials if x['id'] == tutorial_id), None)
    params = request.json
    if not item:
        return {'message': 'No tutorials with this id'}, 400
    item.update(params)
    return item


@app.route('/tutorials/<int:tutorial_id>', methods=['DELETE'])
def delete_tutorial(tutorial_id):
    idx, _ = next((x for x in enumerate(tutorials) if x[1]['id'] ==
                   tutorial_id), (None, None))
    tutorials.pop(idx)
    return '', 204

# @app.route('/user/<username>')
# def profile(username):
#     return '{}\'s profile'.format(escape(username))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],[request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#         error = 'Invalid username/password'
#     return render_template('login.html', error=error)


# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('login'))
#     print(url_for('login', next='/'))
#     print(url_for('profile', username='John Doe'))
