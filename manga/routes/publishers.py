from flask import render_template, url_for, redirect, Blueprint, request
from manga.models.publishers import select_Publishers, add_Publisher, delete_Publisher, update_Publisher

Publishers = Blueprint('Publishers', __name__)

@Publishers.route('/publishers', methods=['GET'])
def publishers():
    publishers = select_Publishers()
    return render_template('publishers.html', title='Publishers', publishers=publishers)

@Publishers.route('/publishers/add', methods=['POST'])
def add():
    publisher = request.form['publisher']
    add_Publisher(publisher)
    return redirect('/publishers')

@Publishers.route('/publishers/delete', methods=['POST'])
def delete():
    publisher = request.form['key']
    delete_Publisher(publisher)
    return redirect('/publishers')

@Publishers.route('/publishers/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        key = request.form['key']
        data = request.form['publisher']
        update_Publisher(key, data)
    return redirect('/publishers')