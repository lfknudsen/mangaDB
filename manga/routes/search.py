from flask import render_template, url_for, redirect, Blueprint, request
from manga.models.settings import settings_sort
from manga.models.search import search

Search = Blueprint('Search', __name__)

@Search.route('/search', methods=['GET', 'POST'])
def series_search():
    if request.method == 'POST':
        sort = settings_sort()
        series = search(request.form['search'], sort)
    return render_template('series.html', title='Manga Series', series=series, sort=sort)