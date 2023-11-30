from flask import render_template, url_for, redirect, Blueprint, request
from manga.models.volumes import select_Volumes, add_Volume, remove_Volume
from manga.models.volumes import select_Volumes_By_Series

Volumes = Blueprint('Manga Volumes', __name__)

@Volumes.route('/volumes', methods=['GET', 'POST'])
def volumes():
    volumes = select_Volumes()
    return render_template('volumes.html', title='Manga Volumes', volumes=volumes)

@Volumes.route('/volumes/add', methods=['POST'])
def add():
    if request.method == 'POST':
        volume_info = [request.form['name'], request.form.get('entry', type=int), request.form['series_year']]
        if volume_info[0] != None and volume_info[1] != None:
            add_Volume(volume_info)
        return redirect('/volumes')

@Volumes.route('/volumes/add/multiple', methods=['POST'])
def add_multiple():
    if request.method == 'POST':
        print('Reached post - insert multiple')
        volume_info = [request.form['name'], request.form['series_year'],
            request.form.get('start_entry', type=int), request.form.get('last_entry', type=int)]

        if volume_info[0] != None and volume_info[1] != None and volume_info[3] > volume_info[2]:
            for entry in range(volume_info[2], volume_info[3] + 1):
                add_Volume([ volume_info[0], entry, volume_info[1] ])

        return redirect('/volumes')

@Volumes.route('/volumes/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        volume_info = [request.form['name'], request.form['series_year'], request.form.get('entry', type=int)]
        if volume_info[2] != None:
            remove_Volume(volume_info)
        return redirect('/volumes')

@Volumes.route('/volumes/<string:series>/<string:series_year>', methods=['GET'])
def volumes_by_series(series, series_year):
    volumes = select_Volumes_By_Series(series, series_year)
    return render_template('volumes.html', title='Manga Volumes', volumes=volumes)