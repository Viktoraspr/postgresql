"""
There are all info about tables in DB.
"""

from dataclasses import dataclass

from .columns_names_DB import *
from .files_names import raw_titles, raw_credits, best_show_by_year, best_movies_by_year


@dataclass
class Column:
    """
    This class creates instance about column: name, column type.
    """
    name: str
    data_type: type = None


AGE_CERTIFICATION_COLUMN = Column(name=AGE_CERTIFICATION, data_type=str)
CHARACTER_COLUMN = Column(name=CHARACTER, data_type=str)
DURATION_COLUMN = Column(name=DURATION, data_type=str)
GENRE_COLUMN = Column(name=GENRE, data_type=str)
FILM_ID_COLUMN = Column(name=FILM_ID, data_type=str)
IMDB_ID_COLUMN = Column(name=IMDB_ID, data_type=str)
IMDB_SCORE_COLUMN = Column(name=IMDB_SCORE, data_type=str)
IMDB_VOTES_COLUMN = Column(name=IMDB_VOTES, data_type=str)
INDEX_COLUMN = Column(name=INDEX, data_type=int)
MAIN_GENRE_COLUMN = Column(name=MAIN_GENRE, data_type=int)
MAIN_PRODUCTION_COLUMN = Column(name=MAIN_PRODUCTION, data_type=int)
NAME_COLUMN = Column(name=NAME, data_type=int)
NUMBER_OF_SEASONS_COLUMN = Column(name=NUMBER_OF_SEASONS, data_type=int)
NUMBER_OF_VOTES_COLUMN = Column(name=NUMBER_OF_VOTES, data_type=int)
PERSON_ID_COLUMN = Column(name=PERSON_ID, data_type=int)
PRODUCTION_COUNTRIES_COLUMN = Column(name=PRODUCTION_COUNTRIES, data_type=int)
RELEASE_YEAR_COLUMN = Column(name=RELEASE_YEAR, data_type=int)
ROLE_COLUMN = Column(name=ROLE, data_type=str)
RUNTIME_COLUMN = Column(name=RUNTIME, data_type=str)
SCORE_COLUMN = Column(name=SCORE, data_type=str)
SEASONS_COLUMN = Column(name=SEASONS, data_type=str)
TITLE_COLUMN = Column(name=TITLE, data_type=str)
TYPE_COLUMN = Column(name=TYPE, data_type=str)

ACTORS_TABLE_NAME = 'actors'
BEST_MOVIES_BY_YEAR_TABLE_NAME = 'best_movies_by_year'
BEST_SHOWS_BY_YEAR_TABLE_NAME = 'best_shows_by_year'
CHARACTERS_TABLE_NAME = 'characters'
GENRES_TABLE_NAME = 'genres'
GENRES_TITLES_TABLE_NAME = 'genres_titles'
MOVIES_TABLE_NAME = 'movies'
PRODUCTION_COUNTRIES_TABLE_NAME = 'production_countries'
PRODUCTION_COUNTRIES_TITLES_TABLE_NAME = 'production_countries_titles'
ROLES_TABLE_NAME = 'roles'


@dataclass
class Table:
    """
    This class creates instance about Table: name, columns, index_label - primary key.
    """
    name: str
    csv_file_name: str
    columns: tuple[Column, ...]
    primary_key: Column | tuple[Column, ...]
    columns_value_must_be: Column | tuple[Column, ...] = None


# All tables to convert DB to 2nd NF.
genres_table = Table(
    name=GENRES_TABLE_NAME,
    columns=(Column(f'{GENRE}_id'), GENRE_COLUMN),
    csv_file_name=raw_titles,
    primary_key=Column(f'{GENRE}_id'),
)

production_countries_table = Table(
    name=PRODUCTION_COUNTRIES_TABLE_NAME,
    columns=(Column(f'{PRODUCTION_COUNTRIES}_id'), PRODUCTION_COUNTRIES_COLUMN,),
    csv_file_name=raw_titles,
    primary_key=Column(f'{PRODUCTION_COUNTRIES}_id'),
)

movies_table = Table(
    name=MOVIES_TABLE_NAME,
    csv_file_name=raw_titles,
    columns=(FILM_ID_COLUMN, TITLE_COLUMN, TYPE_COLUMN, RELEASE_YEAR_COLUMN, AGE_CERTIFICATION_COLUMN,
             RUNTIME_COLUMN, SEASONS_COLUMN, IMDB_ID_COLUMN, IMDB_SCORE_COLUMN, IMDB_VOTES_COLUMN),
    primary_key=Column(FILM_ID),
)

actors_table = Table(
    name=ACTORS_TABLE_NAME,
    csv_file_name=raw_credits,
    columns=(PERSON_ID_COLUMN, NAME_COLUMN),
    primary_key=Column(PERSON_ID),
)

characters_table = Table(
    name=CHARACTERS_TABLE_NAME,
    csv_file_name=raw_credits,
    columns=(FILM_ID_COLUMN, PERSON_ID_COLUMN, CHARACTER_COLUMN),
    primary_key=(PERSON_ID_COLUMN, FILM_ID_COLUMN, CHARACTER_COLUMN)
)

roles_table = Table(
    name=ROLES_TABLE_NAME,
    csv_file_name=raw_credits,
    columns=(FILM_ID_COLUMN, PERSON_ID_COLUMN, ROLE_COLUMN),
    primary_key=(PERSON_ID_COLUMN, FILM_ID_COLUMN, ROLE_COLUMN)
)

best_shows_by_year = Table(
    name=BEST_SHOWS_BY_YEAR_TABLE_NAME,
    csv_file_name=best_show_by_year,
    columns=(TITLE_COLUMN,),
    primary_key=FILM_ID_COLUMN
)

best_movies_by_year = Table(
    name=BEST_MOVIES_BY_YEAR_TABLE_NAME,
    csv_file_name=best_movies_by_year,
    columns=(TITLE_COLUMN,),
    primary_key=FILM_ID_COLUMN
)

ALL_DB_TABLES = [GENRES_TITLES_TABLE_NAME, BEST_SHOWS_BY_YEAR_TABLE_NAME, BEST_MOVIES_BY_YEAR_TABLE_NAME,
                 GENRES_TABLE_NAME, CHARACTERS_TABLE_NAME, ACTORS_TABLE_NAME, ROLES_TABLE_NAME,
                 PRODUCTION_COUNTRIES_TITLES_TABLE_NAME, PRODUCTION_COUNTRIES_TABLE_NAME, MOVIES_TABLE_NAME]

TABLES_FROM_COLUMN_LIST = [genres_table, production_countries_table]

TABLES_WITH_FOREIGN_KEYS = [PRODUCTION_COUNTRIES_TITLES_TABLE_NAME, GENRES_TITLES_TABLE_NAME]
