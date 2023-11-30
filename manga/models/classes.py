class Volume_Key(tuple):
    def __init__(self, volume_data):
        self.name = volume_data[0]
        self.series_year = volume_data[1]
        self.entry = volume_data[2]

class Volume():
    def __init__(self, Volume_Key, authors):
        self.name = Volume_Key.name
        self.series_year = Volume_Key.series_year
        self.entry = Volume_Key.entry
        self.authors = authors

class Series(tuple):
    def __init__(self, series_data):
        self.name = series_data[0]
        self.series_year = series_data[1]
        self.volumes = series_data[2]
        self.rating = series_data[3]
        self.language = series_data[4]
        self.demographic = series_data[5]
        self.publisher = series_data[6]

class Series_with_Authors():
    def __init__(self, key, authors):
        self.name = key[0]
        self.series_year = key[1]
        self.volumes = key[2]
        self.rating = key[3]
        self.language = key[4]
        self.demographic = key[5]
        self.publisher = key[6]
        self.authors = authors

class Author(tuple):
    def __init__(self, author_data):
        self.name = author_data[0]

class Series_Full(tuple):
    def __init__(self, series_data):
        self.name = series_data[0]
        self.series_year = series_data[1]
        self.author = series_data[2]
        self.edition = series_data[3]
        self.rating = series_data[4]
        self.language = series_data[5]
        self.demographic = series_data[6]
        self.publisher = series_data[7]

class Author_with_Series_Count(tuple):
    def __init__(self, author_data):
        self.author = author_data[0]
        self.series_count = author_data[1]

class Demographic(tuple):
    def __init__(self, demo_data):
        self.demo = demo_data[0]
        self.desc = demo_data[1]
        self.series_count = demo_data[2]

class Sort_Settings(tuple):
    def __init__(self, sort_info):
        self.category = sort_info[0]
        self.direction = sort_info[1]

class Language(tuple):
    def __init__(self, lang_data):
        self.language = lang_data[0]
        self.series_count = lang_data[1]

class Publisher(tuple):
    def __init__(self, pub_data):
        self.publisher = pub_data[0]
        self.series_count = pub_data[1]

class Genre(tuple):
    def __init__(self, genre_data):
        self.genre = genre_data[0]
        self.series_count = genre_data[1]