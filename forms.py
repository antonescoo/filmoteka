from flask_admin.form import ImageUploadField
from wtforms import Form, StringField, TextAreaField

class FilmForm(Form):
    name = StringField('Название')
    # genres_genre_id = 3
    director = StringField('Режиссёр')
    description = TextAreaField('Описание')
    # rating = db.Column(db.Integer)
    poster = ImageUploadField('Добавить постер')
