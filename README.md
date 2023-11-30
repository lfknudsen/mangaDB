# Manga Database Management App

## Background
Got bronchitis, made this.
It's a Flask web app which provides a UI for managing a PostgreSQL database of manga/comic books. Excel can work for this purpose, but I find it lacking in a few areas, making it unable to compare to actual database software... like this app!
It has a rudimentary search function and a plain but pretty enough UI.

## Running it yourself
To run it yourself, you'll need Flask, Flask_bcrypt, Flask_login, Flask_wtf, wtforms, PostgreSQL, Python and Psycopg2. Install and run everything through the Linux Subsystem if you're on Windows (not technically necessary, but easier).
The following tutorial to get it running was initially written by Pax, a TA on the course Udvikling af Informationssystemer.\
Mac-users will just write "psql" instead of "psql -U postgres".\
\
To initialise the database:\
Go to the flask_app folder. $ indicates a command.\
(Windows only:) $ sudo service postgresql start\
$ psql -U postgres\
$ CREATE DATABASE mangadb;\
$ ALTER USER postgres PASSWORD '123'; -- Adjust this to whatever you want, just be sure to also adjust __init__.py.\
$ \\q\
$ cd manga\
$ psql -U postgres -d manga\
$ \\i schema.sql\
(Optionally) To enter some default values that I designed, type\
$ \\i schema_ins.sql\
\
$ \\q\
\
Now to run the application itself. In the same terminal, go back up to the flask_app folder, and then:\
$ python3 run.py\
\
If this does not work, try:\
$ export FLASK_APP=run.py\
$ export FLASK_ENV=development\
$ export FLASK_RUN_PORT=5000   (or any other port number)\
$ flask run\
If you close Flask, you need only type the final line in the future.\
\
Finally, go to your browser and type in 127.0.0.1:5000 (or localhost:5000) and you should see the website. Enjoy.\
