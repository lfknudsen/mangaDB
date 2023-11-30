from manga import connection
from psycopg2 import sql

from manga.models.classes import Series, Series_Full, Series_with_Authors

def Filter(filter_type, filter):
    if (filter_type == 'genre'):
        return ("""
        LEFT JOIN Genre_Of
            ON Series.name=Genre_Of.series AND Series.series_year=Genre_Of.series_year
        WHERE genre='""" + filter + "'")
    elif (filter_type == 'demographic'):
        return ("WHERE demo='" + filter + "'")
    elif (filter_type == '' or filter_type == None):
        return ""
    else:
        return ("WHERE " + filter_type + "='" + filter + "'")

def Order_By(sort):
    if (sort.category == 'name, series_year' and sort.direction == 'DES'):
        return """ 
        ORDER BY name DESC, series_year DESC
        """
    elif (sort.category == 'rating' and sort.direction == 'ASC'):
        return """ 
        ORDER BY Series.rating ASC, name ASC, series_year ASC
        """
    elif (sort.category == 'rating' and sort.direction == 'DES'):
        return """ 
        ORDER BY Series.rating DESC, name ASC, series_year ASC
        """
    elif (sort.category == 'owned' and sort.direction == 'ASC'):
        return """ 
        ORDER BY COUNT(entry) ASC, name ASC, series_year ASC
        """
    elif (sort.category == 'owned' and sort.direction == 'DES'):
        return """ 
        ORDER BY COUNT(entry) DESC, name ASC, series_year ASC
        """
    elif (sort.category == 'language' and sort.direction == 'ASC'):
        return """ 
        ORDER BY language ASC, name ASC, series_year ASC
        """
    elif (sort.category == 'language' and sort.direction == 'DES'):
        return """ 
        ORDER BY language DESC, name ASC, series_year ASC
        """
    elif (sort.category == 'demographic' and sort.direction == 'ASC'):
        return """ 
        ORDER BY demo ASC, name ASC, series_year ASC
        """
    elif (sort.category == 'demographic' and sort.direction == 'DES'):
        return """ 
        ORDER BY demo DESC, name ASC, series_year ASC
        """
    elif (sort.category == 'publisher' and sort.direction == 'ASC'):
        return """ 
        ORDER BY publisher ASC, name ASC, series_year ASC
        """
    elif (sort.category == 'publisher' and sort.direction == 'DES'):
        return """ 
        ORDER BY publisher DESC, name ASC, series_year ASC
        """
    else:
        return """ 
        ORDER BY name ASC, series_year ASC
        """

def select_Series(sort):
    cursor = connection.cursor()
    sql = """
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
        GROUP BY (Series.name, Series.series_year, language, demo, publisher)
    """
    sql += Order_By(sort)

    cursor.execute(sql,)
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

def add_Series(series, series_year):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    INSERT INTO Series(name, series_year)
    VALUES(%s, %s)
    """)
    cursor.execute(user_sql, (series, series_year))
    connection.commit()
    cursor.close()

def delete_Series(input):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    DELETE FROM Series
    WHERE name=%s AND series_year=%s
    """)
    cursor.execute(user_sql, (input[0], input[1]))
    connection.commit()
    cursor.close()

def select_Specific_Series(input):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    SELECT Series.name, Series.series_year, Authorship.author, edition, rating, language, demo, publisher
    FROM (Series LEFT JOIN Authorship ON Series.name=Authorship.series AND Series.series_year=Authorship.series_year)
    LEFT JOIN Language_Of
    ON Series.name=Language_Of.series AND Series.series_year=Language_Of.series_year
    LEFT JOIN Demographic_Of
    ON Series.name=Demographic_Of.series AND Series.series_year=Demographic_Of.series_year
    LEFT JOIN Publisher_Of
    ON Series.name=Publisher_Of.series AND Series.series_year=Publisher_Of.series_year
    WHERE Series.name=%s AND Series.series_year=%s
    """)
    cursor.execute(user_sql, (input[0], input[1]))
    results = cursor.fetchall()
    cursor.close()
    series = []
    for s in results:
        series.append(Series_Full(s))
    return series

def select_Series_by_Author(name, sort):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    SELECT Series.name, Series.series_year, COUNT(entry), Series.rating, language, demo, publisher
    FROM Authorship
    LEFT JOIN Volumes
        ON Authorship.series=Volumes.name AND Authorship.series_year=Volumes.series_year
    LEFT JOIN Series
        ON Series.name=Authorship.series AND Series.series_year=Authorship.series_year
    LEFT JOIN Language_Of
        ON Series.name=Language_Of.series AND Series.series_year=Language_Of.series_year
    LEFT JOIN Demographic_Of
        ON Series.name=Demographic_Of.series AND Series.series_year=Demographic_Of.series_year
    LEFT JOIN Publisher_Of
        ON Series.name=Publisher_Of.series AND Series.series_year=Publisher_Of.series_year
    WHERE author=%s
    GROUP BY (Series.name, Series.series_year, Series.rating, language, demo, publisher)
    """
    + Order_By(sort))
    cursor.execute(user_sql, (name,))
    results = cursor.fetchall()
    series = []
    for s in results:
        series.append(Series(s))

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

def select_Series_by_Filter(filter_type, filter, sort):
    cursor = connection.cursor()
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
    """
    + Filter(filter_type, filter)
    + """
    GROUP BY (Series.name, Series.series_year, Series.rating, language, demo, publisher)
    """
    + Order_By(sort))
    cursor.execute(user_sql, (filter_type, filter))
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

def select_Series_by_Genre(genre, sort):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    SELECT Series.name, Series.series_year, COUNT(entry), Series.rating, language, demo, publisher
    FROM Genre_Of
    LEFT JOIN Volumes
        ON Genre_Of.series=Volumes.name AND Genre_Of.series_year=Volumes.series_year
    LEFT JOIN Series
        ON Series.name=Genre_Of.series AND Series.series_year=Genre_Of.series_year
    LEFT JOIN Language_Of
        ON Series.name=Language_Of.series AND Series.series_year=Language_Of.series_year
    LEFT JOIN Demographic_Of
        ON Series.name=Demographic_Of.series AND Series.series_year=Demographic_Of.series_year
    LEFT JOIN Publisher_Of
        ON Series.name=Publisher_Of.series AND Series.series_year=Publisher_Of.series_year
    WHERE genre=%s
    GROUP BY (Series.name, Series.series_year, Series.rating, language, demo, publisher)
    """
    + Order_By(sort))
    cursor.execute(user_sql, (genre,))
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

def select_Series_by_Language(language, sort):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    SELECT Series.name, Series.series_year, COUNT(entry), Series.rating, language, demo, publisher
    FROM Language_Of
    LEFT JOIN Volumes
        ON Language_Of.series=Volumes.name AND Language_Of.series_year=Volumes.series_year
    LEFT JOIN Series
        ON Series.name=Language_Of.series AND Series.series_year=Language_Of.series_year
    LEFT JOIN Demographic_Of
        ON Series.name=Demographic_Of.series AND Series.series_year=Demographic_Of.series_year
    LEFT JOIN Publisher_Of
        ON Series.name=Publisher_Of.series AND Series.series_year=Publisher_Of.series_year
    WHERE language=%s
    GROUP BY (Series.name, Series.series_year, Series.rating, language, demo, publisher)
    """
    + Order_By(sort))
    cursor.execute(user_sql, (language,))
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

def select_Series_by_Demographic(demographic, sort):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    SELECT Series.name, Series.series_year, COUNT(entry), Series.rating, language, demo, publisher
    FROM Demographic_Of
    LEFT JOIN Volumes
        ON Demographic_Of.series=Volumes.name AND Demographic_Of.series_year=Volumes.series_year
    LEFT JOIN Series
        ON Series.name=Demographic_Of.series AND Series.series_year=Demographic_Of.series_year
    LEFT JOIN Language_Of
        ON Series.name=Language_Of.series AND Series.series_year=Language_Of.series_year
    LEFT JOIN Publisher_Of
        ON Series.name=Publisher_Of.series AND Series.series_year=Publisher_Of.series_year
    WHERE demo=%s
    GROUP BY (Series.name, Series.series_year, Series.rating, language, demo, publisher)
    """
    + Order_By(sort))
    cursor.execute(user_sql, (demographic,))
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

def select_Series_by_Publisher(publisher, sort):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    SELECT Series.name, Series.series_year, COUNT(entry), Series.rating, language, demo, publisher
    FROM Publisher_Of
    LEFT JOIN Volumes
        ON Publisher_Of.series=Volumes.name AND Publisher_Of.series_year=Volumes.series_year
    LEFT JOIN Series
        ON Series.name=Publisher_Of.series AND Series.series_year=Publisher_Of.series_year
    LEFT JOIN Language_Of
        ON Series.name=Language_Of.series AND Series.series_year=Language_Of.series_year
    LEFT JOIN Demographic_Of
        ON Series.name=Demographic_Of.series AND Series.series_year=Demographic_Of.series_year
    WHERE publisher=%s
    GROUP BY (Series.name, Series.series_year, Series.rating, language, demo, publisher)
    """
    + Order_By(sort))
    cursor.execute(user_sql, (publisher,))
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

def check_Series_Exists(series, series_year):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    SELECT * FROM Series
    WHERE name=%s AND series_year=%s
    """)
    cursor.execute(user_sql, (series, series_year))
    result = cursor.fetchone()
    cursor.close()
    return (result != None)

def series_Update_Edition(series, series_year, edition):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    UPDATE Series
    SET edition=%s
    WHERE name=%s AND series_year=%s
    """)
    cursor.execute(user_sql, (edition, series, series_year))
    connection.commit()
    cursor.close()

def series_Update_Rating(series, series_year, rating):
    cursor = connection.cursor()
    user_sql = sql.SQL ("""
    UPDATE Series
    SET rating=%s
    WHERE name=%s AND series_year=%s
    """)
    cursor.execute(user_sql, (rating, series, series_year))
    connection.commit()
    cursor.close()