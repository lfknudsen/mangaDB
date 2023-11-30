from manga import connection
from psycopg2 import sql

from manga.models.classes import Sort_Settings

def settings_sort():
    cursor = connection.cursor()
    sql = """
    SELECT sort_category, sort_direction FROM Settings
    """
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    settings = Sort_Settings(result)
    return settings

def update_sort(category):
    cursor = connection.cursor()
    current_settings = settings_sort()
    if current_settings.category == category and current_settings.direction == 'ASC':
        user_sql = sql.SQL ("""
        UPDATE Settings
        SET sort_direction='DES'
        WHERE id=1
        """)
    elif current_settings.category == category and current_settings.direction == 'DES':
        user_sql = sql.SQL ("""
        UPDATE Settings
        SET sort_direction='ASC'
        WHERE id=1
        """)
    else:
        user_sql = sql.SQL ("""
        UPDATE Settings
        SET sort_category=%s, sort_direction='ASC'
        WHERE id=1
        """)
    cursor.execute(user_sql, (category,))
    connection.commit()
    cursor.close()