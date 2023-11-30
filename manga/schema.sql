\i schema_drop.sql

CREATE TABLE IF NOT EXISTS Authors(
    name varchar(120) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Series(
    name varchar(120),
    series_year char(4),
    edition varchar(120),
    rating integer DEFAULT 0,
    demographic varchar(120),
    PRIMARY KEY (name, series_year)
);

CREATE TABLE IF NOT EXISTS Authorship(
    author varchar(120),
    series varchar(120),
    series_year char(4),
    CONSTRAINT fk_author
        FOREIGN KEY (author)
        REFERENCES Authors(name)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_series
        FOREIGN KEY (series, series_year)
        REFERENCES Series(name, series_year)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Volumes(
    name varchar(120) NOT NULL,
    series_year char(4),
    entry integer DEFAULT 1,
    isbn varchar(120) UNIQUE,
    read_status boolean DEFAULT FALSE,
    CONSTRAINT fk_series
        FOREIGN KEY (name, series_year)
        REFERENCES Series(name, series_year)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    PRIMARY KEY (entry, name, series_year)
);

CREATE TABLE IF NOT EXISTS Genres(
    genre varchar(120) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Genre_Of(
    genre varchar(120) REFERENCES Genres(genre)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    series varchar(120),
    series_year char(4),
    CONSTRAINT fk_series
        FOREIGN KEY (series, series_year)
        REFERENCES Series(name, series_year)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Languages(
    language varchar(120) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Language_Of(
    language varchar(120) REFERENCES Languages(language)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    series varchar(120),
    series_year char(4),
    CONSTRAINT fk_series
        FOREIGN KEY (series, series_year)
        REFERENCES Series(name, series_year)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Demographics(
    demo varchar(120) PRIMARY KEY,
    description varchar(240)
);

CREATE TABLE IF NOT EXISTS Demographic_Of(
    demo varchar(120) REFERENCES Demographics(demo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    series varchar(120),
    series_year char(4),
    CONSTRAINT fk_series
        FOREIGN KEY (series, series_year)
        REFERENCES Series(name, series_year)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Publishers(
    publisher varchar(120) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Publisher_Of(
    publisher varchar(120) REFERENCES Publishers(publisher)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    series varchar(120),
    series_year char(4),
    CONSTRAINT fk_series
        FOREIGN KEY (series, series_year)
        REFERENCES Series(name, series_year)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE SEQUENCE User_ID_seq;

CREATE TABLE IF NOT EXISTS Settings(
    id integer DEFAULT nextval('User_ID_seq') PRIMARY KEY,
    sort_category varchar(120) NOT NULL DEFAULT 'name, series_year',
    sort_direction char(3) NOT NULL DEFAULT 'ASC'
)