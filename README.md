# Manga/Book/Comic Book Database Management App

## Background
Got bronchitis, made this.

It's a Flask web app which provides an intuitive user interface for managing a self-hosted PostgreSQL database of manga, comic books, and/or books. I got the idea after seeing a video of a woman who read several hundred volumes of manga a year, and had an understandably enormous collection... which she managed with Excel. I tried to follow her lead and use Excel for this myself, but while I suppose it _can_ work, I find it lacking in a few key areas, making it unable to compare to actual database software... like this app!

It has a rudimentary search function and a plain but pretty enough UI.

## How it works in brief
A Postgres database stores the information you provide it on books/comics/manga that you own.\
The Flask programme runs _this_ programme (including its backing database) in the background on your computer, making it accessible via a particular port.\
You use the programme through your internet browser of choice.

## Requirements
To run it yourself, you'll need
* Flask
* Flask_bcrypt
* Flask_login
* Flask_wtf
* wtforms
* PostgreSQL
* Python
* Psycopg2

If you're on Windows, it will likely be easiest to install and run everything through the Linux Subsystem (WSL).

## Setup & Use
The following tutorial to get it running was initially written by Pax, a TA on the course _Udvikling af Informationssystemer_ ("Development of Information Systems") at the University of Copenhagen. I believe it's been split into two separate courses since then, but I am unsure as to their names.\
The commands below are written for GNU/Linux and Windows. On **MacOS**, use "`psql`" instead of "`psql -U postgres`".

### One-time Setup
To initialise the database, open a terminal emulator of your choice, and go to the `flask_app` directory.\
Note that some of the commands are typed into a Postgres interactive shell which must end with the semi-colon as written below.\
(Windows only:) `$ sudo service postgresql start`\
`psql -U postgres`\
`CREATE DATABASE mangadb;`\
`ALTER USER postgres PASSWORD '123';` -- Change the password to whatever you want, just be sure to adjust `__init__.py` accordingly.\
`\q`\
`cd manga`\
`psql -U postgres -d manga`\
`\i schema.sql`\
(Optionally) To enter some default values that I designed, type\
`\i schema_ins.sql`\
\
`\q`

### Start the application
Now to run the application itself. In the same terminal, go back up to the flask_app folder, and then:\
`python3 run.py`\
\
If this does not work, you may have to configure Flask as follows:\
`export FLASK_APP=run.py`\
`export FLASK_ENV=development`\
`export FLASK_RUN_PORT=5000`   (or any other port number)\
`flask run`\
If you close Flask, you need only type the final line in the future.

### Use the application
Finally, go to your browser and type in
`127.0.0.1:5000` or `localhost:5000` in the address field, and you should see the web application.

## Security Concerns
The application is unlikely to be very safe against deliberate attacks; this was developed before I learned about SQL injection, and so any security against it is from defensive measures in the libraries I've used, rather than by deliberate action on my part as the programmer. I prefer to err on the side of caution, so I recommend not running this application on a port open to the internet.
