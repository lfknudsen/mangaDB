from manga import connection
from psycopg2 import sql

from manga.models.series import Order_By
from manga.models.classes import Series, Series_with_Authors

def Attempt_Rating(term):
    try:
        return int(term)
    except ValueError:
        return None

def search(term, sort):
    cursor = connection.cursor()
    vague_term = "%" + term + "%"
    term_list = [vague_term, term, vague_term, vague_term, vague_term, vague_term, vague_term]
    int_term = Attempt_Rating(term)
    if (int_term != None):
        where_rating = """
        OR Series.rating = %s"""
        term_list.append(int_term)
    else:
        where_rating = ""

    user_sql = sql.SQL ("""
    SELECT Series.name, Series.series_year, COUNT(entry), Series.rating, language, demo, publisher
    FROM Series
        LEFT JOIN Volumes
            ON Series.name=Volumes.name AND Series.series_year=Volumes.series_year
        LEFT JOIN Language_Of
            ON Series.name=Language_Of.series AND Series.series_year=Language_Of.series_year
        LEFT JOIN Demographic_Of
            ON Series.name=Demographic_Of.series AND Series.series_year=Demographic_Of.series_year
        LEFT JOIN Publisher_Of
            ON Series.name=Publisher_Of.series AND Series.series_year=Publisher_Of.series_year
        LEFT JOIN Genre_Of
            ON Series.name=Genre_Of.series AND Series.series_year=Genre_Of.series_year
        LEFT JOIN Authorship
            ON Series.name=Authorship.series AND Series.series_year=Authorship.series_year
    WHERE Series.name LIKE %s
        OR Series.series_year=%s
        OR language LIKE %s
        OR demo LIKE %s
        OR publisher LIKE %s
        OR genre LIKE %s
        OR author LIKE %s
    """
    + where_rating
    + """
    GROUP BY (Series.name, Series.series_year, Series.rating, language, demo, publisher)"""
    + Order_By(sort))

    cursor.execute(user_sql, term_list)
    results = cursor.fetchall()
    series = []
    for r in results:
        series.append(Series(r))

    final_results = []
    for s in series:
        user_sql = ("""
        SELECT author FROM Authorship WHERE series=%s AND series_year=%s
        ORDER BY author ASC
        """)
        cursor.execute(user_sql, (s.name, s.series_year))
        authors = cursor.fetchall()
        author_list = []
        for a in authors:
            author_list.append(a[0])
        final_results.append(Series_with_Authors(s, author_list))

    cursor.close()
    return final_results