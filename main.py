"""
This file we use for DB/File(csv-->Pandas) management.
"""
from constants.db_csv_data import TABLES_FROM_COLUMN_LIST, movies_table, TABLES_WITH_FOREIGN_KEYS, \
    actors_table, characters_table, roles_table, best_shows_by_year, best_movies_by_year
from constants.foreign_keys import tables_foreign_keys
from db_modules.db_management_pandas import DBManagement
from db_modules.file_management import FileManagement
from db_modules.manage_csv_file import CSVFileCorrection
from constants.files_names import ALL_FILES
from constants.db_csv_data import ALL_DB_TABLES

# Creates cleaned new .csv file
files = ALL_FILES
for file_name in files:
    file = CSVFileCorrection(file_name)
    file.lower_column_names()
    file.change_column_name(old_name='id', new_name='film_id')
    file.write_new_data_to_csv_file()


# Drops tables if they exist.
db = DBManagement()
db.drop_table(tables=ALL_DB_TABLES)


for table in TABLES_FROM_COLUMN_LIST:
    file = FileManagement(table)
    file.create_table_with_list_in_one_cell()
    file.create_bridge_table()


file = FileManagement(movies_table)
file.create_table_with_selected_columns(drop=False)
file.create_foreign_keys(TABLES_WITH_FOREIGN_KEYS)

tables = [actors_table, characters_table, roles_table]
for table in tables:
    file = FileManagement(table)
    file.create_table_with_selected_columns()

tables = [best_shows_by_year, best_movies_by_year]
for table in tables:
    file = FileManagement(table)
    file.create_table_with_one_column()

for table in tables_foreign_keys:
    FileManagement.create_foreign_key(data=table)
