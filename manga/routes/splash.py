from flask import render_template, url_for, redirect, Blueprint

Splash = Blueprint('Splash', __name__)

@Splash.route('/', methods=['GET', 'POST'])
def root():
    return render_template('splash.html', title='Splash')