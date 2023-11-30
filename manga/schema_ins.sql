INSERT INTO Authors(name)
VALUES ('Akira Toriyama'), ('Eiichiro Oda'), ('Hiromu Arakawa');

INSERT INTO Series(name, series_year)
VALUES  ('Dragonball', '2003'),
        ('One Piece', '2003');

INSERT INTO Series(name, series_year, edition)
VALUES ('Fullmetal Alchemist', '2018', 'Fullmetal Edition');

INSERT INTO Authorship(author, series, series_year)
VALUES
    ('Akira Toriyama', 'Dragonball', '2003'),
    ('Eiichiro Oda', 'One Piece', '2003'),
    ('Hiromu Arakawa', 'Fullmetal Alchemist', '2018');

INSERT INTO Volumes(name, series_year, entry)
VALUES
    ('Dragonball', '2003', 1),
    ('Dragonball', '2003', 2),
    ('Dragonball', '2003', 3),
    ('One Piece', '2003', 1),
    ('Fullmetal Alchemist', '2018', 1)
;

INSERT INTO Genres(genre)
VALUES
    ('Adventure'), ('Action'), ('Martial Arts'), ('Wholesome'),
    ('Slice of Life'), ('Isekai'), ('Horror')
;

INSERT INTO Genre_Of(genre, series, series_year)
VALUES
    ('Adventure', 'Dragonball', '2003'), ('Action', 'Dragonball', '2003'),
    ('Martial Arts', 'Dragonball', '2003'), ('Adventure', 'One Piece', '2003'),
    ('Action', 'One Piece', '2003'), ('Adventure', 'Fullmetal Alchemist', '2018')
;

INSERT INTO Publishers(publisher)
VALUES ('Viz Media'), ('Kodanshi'), ('Yen Press'), ('Square Enix');

INSERT INTO Publisher_Of(publisher, series, series_year)
VALUES
    ('Viz Media', 'Dragonball', '2003'),
    ('Viz Media', 'One Piece', '2003'),
    ('Viz Media', 'Fullmetal Alchemist', '2018')
;

INSERT INTO Languages(language)
VALUES ('English'), ('Japanese'), ('Danish');

INSERT INTO Language_Of(language, series, series_year)
VALUES
    ('English', 'Dragonball', '2003'),
    ('English', 'One Piece', '2003'),
    ('English', 'Fullmetal Alchemist', '2018')
;

INSERT INTO Demographics(demo, description)
VALUES
    ('Shonen', 'Teenage boys'),
    ('Shojo', 'Teenage girls'),
    ('Seinen', 'Adult men'),
    ('Josei', 'Adult women')
;

INSERT INTO Demographic_Of(demo, series, series_year)
VALUES
    ('Shonen', 'Dragonball', '2003'),
    ('Shonen', 'One Piece', '2003'),
    ('Shonen', 'Fullmetal Alchemist', '2018')
;

INSERT INTO Settings(sort_category, sort_direction)
VALUES ('name, series_year', 'ASC');