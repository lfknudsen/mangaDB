from manga import connection
from psycopg2 import sql
from manga.models.classes import Language

def add_Language(language):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    INSERT INTO Languages(language)
    VALUES (%s)
    """)
    cursor.execute(user_sql, (language,))
    connection.commit()
    cursor.close()

def delete_Language(language):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    DELETE FROM Languages
    WHERE language=%s
    """)
    cursor.execute(user_sql, (language,))
    connection.commit()
    cursor.close()

def select_Languages():
    cursor = connection.cursor()
    sql = """
    SELECT Languages.language, COUNT(series) FROM Languages
    LEFT JOIN Language_Of
        ON Languages.language=Language_Of.language
    GROUP BY (Languages.language)
    ORDER BY language ASC
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    languages = []
    for language in results:
        languages.append(Language(language))
    return languages

def connect_Language(series, series_year, language):
    if series == "" or series_year == "" or language == "":
        return
    if check_Language_Exists(language) == False:
        add_Language(language)

    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    INSERT INTO Language_Of(series, series_year, language)
    VALUES (%s, %s, %s)
    """)
    cursor.execute(user_sql, (series, series_year, language))
    connection.commit()
    cursor.close()

def disconnect_Language(series, series_year):
    if series == "" or series_year == "":
        return
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    DELETE FROM Language_Of
    WHERE series=%s AND series_year=%s
    """)
    cursor.execute(user_sql, (series, series_year))
    connection.commit()
    cursor.close()


def check_Language_Exists(language):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    SELECT * FROM Languages
    WHERE language=%s
    """)
    cursor.execute(user_sql, (language,))
    result = cursor.fetchone()
    cursor.close()
    return (result != None)

def update_Language(key, new):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    UPDATE Languages
    SET language=%s
    WHERE language=%s
    """)
    cursor.execute(user_sql, (new, key))
    connection.commit()
    cursor.close()