from flask import render_template, url_for, redirect, Blueprint, request
from manga.models.authors import select_Authors, add_Author, delete_Author, connect_Author, update_Author

Authors = Blueprint('Authors', __name__)

@Authors.route('/authors', methods=['GET', 'POST'])
def authors():
    authors = select_Authors()
    return render_template('authors.html', title='Authors', authors=authors)

@Authors.route('/authors/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author_info = [request.form['name']]
        if author_info[0] != None:
            add_Author(author_info[0])
    return redirect('/authors')

@Authors.route('/authors/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        author_info = [request.form['key']]
        if author_info[0] != None:
            delete_Author(author_info[0])
    return redirect('/authors')

@Authors.route('/authors/connect', methods=['POST'])
def connect():
    if request.method == 'POST':
        from_url = request.form['from']
        connect_Author(request.form['name'], request.form['series_year'], request.form['author_name'])
    return redirect(from_url)

@Authors.route('/authors/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        key = request.form['key']
        data = request.form['author']
        update_Author(key, data)
    return redirect('/authors')