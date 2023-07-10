from dataclasses import dataclass

from constants.db_csv_data import characters_table, actors_table, movies_table, best_movies_by_year, \
    best_shows_by_year, roles_table


@dataclass
class ForeignKey:
    child_table_name: str
    parent_table_name: str
    key_column: str


actors_characters = ForeignKey(
    child_table_name=characters_table.name,
    parent_table_name=actors_table.name,
    key_column=actors_table.primary_key.name
)


characters_movies = ForeignKey(
    child_table_name=characters_table.name,
    parent_table_name=movies_table.name,
    key_column=movies_table.primary_key.name
)

best_movies_by_year__movies = ForeignKey(
    child_table_name=best_movies_by_year.name,
    parent_table_name=movies_table.name,
    key_column=movies_table.primary_key.name
)

best_shows_by_year__movies = ForeignKey(
    child_table_name=best_shows_by_year.name,
    parent_table_name=movies_table.name,
    key_column=movies_table.primary_key.name
)

roles__movies = ForeignKey(
    child_table_name=roles_table.name,
    parent_table_name=movies_table.name,
    key_column=movies_table.primary_key.name
)

tables_foreign_keys = [actors_characters, characters_movies, best_movies_by_year__movies, best_shows_by_year__movies,
                       roles__movies]
