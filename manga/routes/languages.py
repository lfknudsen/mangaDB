from flask import render_template, url_for, redirect, Blueprint, request
from manga.models.languages import select_Languages, add_Language, delete_Language, update_Language

Languages = Blueprint('Languages', __name__)

@Languages.route('/languages', methods=['GET'])
def languages():
    languages = select_Languages()
    return render_template('languages.html', title='Languages', languages=languages)

@Languages.route('/languages/add', methods=['POST'])
def add():
    language = request.form['language']
    add_Language(language)
    return redirect('/languages')

@Languages.route('/languages/delete', methods=['POST'])
def delete():
    language = request.form['key']
    delete_Language(language)
    return redirect('/languages')

@Languages.route('/languages/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        key = request.form['key']
        data = request.form['language']
        update_Language(key, data)
    return redirect('/languages')