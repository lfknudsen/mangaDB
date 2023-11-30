from manga import connection
from psycopg2 import sql

from manga.models.classes import Author, Author_with_Series_Count
from manga.models.series import check_Series_Exists, add_Series

def select_Specific_Authors(name):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    SELECT name FROM Authors
    WHERE name=%s
    """)
    cursor.execute(user_sql, (name,))
    results = cursor.fetchall()
    cursor.close()
    authors = []
    for author in results:
        authors.append(Author(author))
    return authors

def add_Author(name):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    INSERT INTO Authors(name)
    VALUES(%s)
    """)
    cursor.execute(user_sql, (name,))
    connection.commit()
    cursor.close()

def select_Authors():
    cursor = connection.cursor()
    sql = """
    SELECT name, Count(series)
    FROM Authors
    LEFT JOIN Authorship
        ON Authors.name=Authorship.author
    GROUP BY (name)
    ORDER BY name ASC
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    authors = []
    for author in results:
        authors.append(Author_with_Series_Count(author))
    return authors

def delete_Author(name):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    DELETE FROM Authors
    WHERE name=%s
    """)
    cursor.execute(user_sql, (name,))
    connection.commit()
    cursor.close()

def select_Authors_of_Series(input):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    SELECT author FROM Authorship WHERE series=%s AND series_year=%s
    ORDER BY author ASC
    """)
    cursor.execute(user_sql, (input[0], input[1]))
    results = cursor.fetchall()
    cursor.close()
    names = []
    for author in results:
        names.append(Author(author))
    return names

def delete_Author_Connection(input):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    DELETE FROM Authorship
    WHERE series=%s AND series_year=%s AND author=%s
    """)
    cursor.execute(user_sql, (input[0], input[1], input[2]))
    connection.commit()
    cursor.close()

def check_Author_Exists(author):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    SELECT * FROM Authors
    WHERE name=%s
    """)
    cursor.execute(user_sql, (author,))
    result = cursor.fetchone()
    cursor.close()
    return (result != None)

def connect_Author(series, series_year, author):
    if series == "" or series_year == "" or author == "":
        return
    if check_Author_Exists(author) == False:
        add_Author(author)
    if check_Series_Exists(series, series_year) == False:
        add_Series(series, series_year)
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    INSERT INTO Authorship(series, series_year, author)
    VALUES (%s, %s, %s)
    """)
    cursor.execute(user_sql, (series, series_year, author))
    connection.commit()
    cursor.close()

def update_Author(key, new):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    UPDATE Authors
    SET name=%s
    WHERE name=%s
    """)
    cursor.execute(user_sql, (new, key))
    connection.commit()
    cursor.close()