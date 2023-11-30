from flask import render_template, url_for, redirect, Blueprint, request
from manga.models.genres import select_Genres, add_Genre, delete_Genre

Edit = Blueprint('Edit', __name__)

@Edit.route('/edit', methods=['GET', 'POST'])
def genres():
    if request.method == "POST":
        table = request.form['table']
        if table == "Demographics": 
            data = [request.form['demo'], request.form['desc']]
        else:
            data = [request.form['data']]
    return render_template('edit.html', title='Edit <string:table>', table=table, data=data)