from flask import render_template, url_for, redirect, Blueprint, request
from manga.models.genres import select_Genres, add_Genre, delete_Genre, update_Genre

Genres = Blueprint('Genres', __name__)

@Genres.route('/genres', methods=['GET'])
def genres():
    genres = select_Genres()
    return render_template('genres.html', title='Genres', genres=genres)

@Genres.route('/genres/add', methods=['POST'])
def add():
    new = request.form['genre_name']
    add_Genre(new)
    return redirect('/genres')

@Genres.route('/genres/delete', methods=['POST'])
def delete():
    genre = request.form['key']
    delete_Genre(genre)
    return redirect('/genres')

@Genres.route('/genres/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        key = request.form['key']
        data = request.form['genre']
        update_Genre(key, data)
    return redirect('/genres')