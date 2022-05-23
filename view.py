from app import app
from app import db
from flask import render_template
from forms import FilmForm

from models import Films

from flask import request
from flask import redirect
from flask import url_for

from flask_security import login_required


@app.route('/create', methods=['POST', 'GET'])
@login_required
def create_film():
    if request.method == 'POST':
        name = request.form['name']
        genres_genre_id = 3
        director = request.form['director']
        description = request.form['description']
        poster = request.form['poster']

        try:
            film = Films(name=name, genres_genre_id=genres_genre_id,
                         director=director, description=description,
                         poster=poster)
            db.session.add(film)
            db.session.commit()

        except:
            print('Что-то пошло не так')

        return redirect(url_for('films'))

    form = FilmForm()
    return render_template('/create_film.html', title='Добавить фильм',
                           form=form)


@app.route('/')
def index():
    return render_template('index.html', title='Главная')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/films', methods=['GET'])
def films():
    q = request.args.get('q')

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        film_list = Films.query.filter(Films.name.contains(q) |
                                       Films.description.contains(q)) #.all()
    else:
        film_list = Films.query.order_by(Films.name.asc())

    pages = film_list.paginate(page=page, per_page=3)

    return render_template('films.html', title='Фильмы', pages=pages)


@app.route('/films/<slug>', methods=['GET'])
def film(slug):
    film = Films.query.filter(Films.slug == slug).first_or_404()
    if not film:
        return {'message': 'No tutorials with this slug'}, 400
    return render_template('film.html', film=film)