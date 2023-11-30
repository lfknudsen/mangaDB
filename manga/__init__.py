from flask import Flask
import psycopg2

app = Flask(__name__)
database = "dbname='mangadb' user='postgres' host='127.0.0.1' password = '123'"
connection = psycopg2.connect(database)

from manga.routes.volumes import Volumes
app.register_blueprint(Volumes)

from manga.routes.splash import Splash
app.register_blueprint(Splash)

from manga.routes.series import Series
app.register_blueprint(Series)

from manga.routes.authors import Authors
app.register_blueprint(Authors)

from manga.routes.genres import Genres
app.register_blueprint(Genres)

from manga.routes.languages import Languages
app.register_blueprint(Languages)

from manga.routes.demographics import Demographics
app.register_blueprint(Demographics)

from manga.routes.publishers import Publishers
app.register_blueprint(Publishers)

from manga.routes.edit import Edit
app.register_blueprint(Edit)

from manga.routes.search import Search
app.register_blueprint(Search)