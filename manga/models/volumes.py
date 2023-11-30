from manga import connection
from psycopg2 import sql

from manga.models.classes import Volume_Key, Volume

def select_Volumes():
    cursor = connection.cursor()
    sql = """
    SELECT Volumes.name, Volumes.series_year, entry
    FROM Volumes
    ORDER BY Volumes.name, Volumes.series_year, entry ASC
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    volumes = []
    for vol in results:
        volumes.append(Volume_Key(vol))

    final_results = []
    for r in volumes:
        user_sql = ("""
        SELECT author FROM Authorship WHERE series=%s AND series_year=%s
        ORDER BY author ASC
        """)
        print(type(r))
        cursor.execute(user_sql, (r.name, r.series_year))
        authors = cursor.fetchall()
        author_list = []
        for a in authors:
            author_list.append(a[0])
        final_results.append(Volume(r, author_list))

    cursor.close()
    return final_results

def add_Volume(user_input):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    INSERT INTO Volumes(name, entry, series_year)
    VALUES(%s, %s, %s)
    """)
    cursor.execute(user_sql, (user_input[0], int(user_input[1]), user_input[2]))
    connection.commit()
    cursor.close()

def remove_Volume(input):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    DELETE FROM Volumes
    WHERE name=%s AND series_year=%s AND entry=%s
    """)
    cursor.execute(user_sql, (input[0], input[1], input[2]))
    connection.commit()
    cursor.close()

def select_Volumes_By_Series(series, series_year):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    SELECT Volumes.name, Volumes.series_year, entry
    FROM Volumes
    WHERE Volumes.name=%s AND Volumes.series_year=%s
    ORDER BY Volumes.name, Volumes.series_year, entry ASC
    """)
    cursor.execute(user_sql, (series, series_year))
    results = cursor.fetchall()
    volumes = []
    for vol in results:
        volumes.append(Volume_Key(vol))

    final_results = []
    for r in volumes:
        user_sql = ("""
        SELECT author FROM Authorship WHERE series=%s AND series_year=%s
        ORDER BY author ASC
        """)
        print(type(r))
        cursor.execute(user_sql, (r.name, r.series_year))
        authors = cursor.fetchall()
        author_list = []
        for a in authors:
            author_list.append(a[0])
        final_results.append(Volume(r, author_list))

    cursor.close()
    return final_results