"""
This file is for testing classes and their methods
"""

import unittest

from sqlalchemy.exc import ProgrammingError

from constants.columns_names_DB import GENRE
from constants.db_csv_data import Table, FILM_ID_COLUMN, TYPE_COLUMN, IMDB_VOTES_COLUMN, Column, GENRE_COLUMN, \
    TITLE_COLUMN
from db_modules.db_management_pandas import DBManagement
from db_modules.file_management import FileManagement
from db_modules.manage_csv_file import CSVFileCorrection


class TestCSVFileCorrection(unittest.TestCase):
    """
    Checking CSVFileCorrection class
    """
    file_name = 'raw_titles_tests.csv'

    def test_csv_file_correction(self):
        """
        Tests for CSVFileCorrection class
        :return: None
        """
        file = CSVFileCorrection(file_name=self.file_name)

        file.change_column_name('title', 'Title')
        self.assertIn('Title', file.raw_data.columns)
        self.assertNotIn('title', file.raw_data.columns)

        file.lower_column_names()

        column: str
        for column in file.raw_data.columns:
            self.assertEquals(column.lower(), column)

        file.write_new_data_to_csv_file()
        file = CSVFileCorrection(file_name=self.file_name)

        column: str
        for column in file.raw_data.columns:
            self.assertEqual(column.lower(), column)


class TestFileManagement(unittest.TestCase):
    """
    Testing FileManagement and DBManagement classes
    """
    file_name = 'raw_titles_tests.csv'
    new_table = Table(
        name='test_table',
        columns=(FILM_ID_COLUMN, TYPE_COLUMN, IMDB_VOTES_COLUMN),
        csv_file_name=file_name,
        primary_key=FILM_ID_COLUMN,
    )
    file_management = FileManagement(table=new_table)

    def test_create_table_with_selected_columns(self):
        """
        Creates test table in DB with selected columns.
        :return: None
        """
        self.file_management.create_table_with_selected_columns()

        columns = [column.name for column in self.new_table.columns]
        data = self.file_management.read_data_using_pandas_framework(table_name='test_table')
        columns_db = list(data.columns)
        rows, _ = data.shape

        self.assertEqual(columns, columns_db)
        self.assertGreater(rows, 1)

    def test_read_data_using_pandas_framework(self):
        """
        Read whole table and only some columns. Check if data exists.
        :return: None
        """
        self.file_management.create_table_with_selected_columns()

        columns = [column.name for column in self.new_table.columns]
        data = self.file_management.read_data_using_pandas_framework(table_name='test_table')
        columns_db = list(data.columns)
        rows, _ = data.shape

        self.assertEqual(columns, columns_db)
        self.assertGreater(rows, 1)

        data = self.file_management.read_data_using_pandas_framework(table_name='test_table')
        columns_db = list(data.columns)
        rows, _ = data.shape

        self.assertEqual(columns, columns_db)
        self.assertGreater(rows, 1)

        less_columns = [FILM_ID_COLUMN.name, TYPE_COLUMN.name]
        data = self.file_management.read_data_using_pandas_framework(table_name='test_table', columns=less_columns)
        columns_db = list(data.columns)
        rows, _ = data.shape

        self.assertEqual(less_columns, columns_db)
        self.assertGreater(rows, 1)

        self.file_management.drop_table([self.new_table.name])
        with self.assertRaises(ProgrammingError):
            self.file_management.read_data_using_pandas_framework(table_name='test_table')

    def test_create_table_with_list_in_one_cell_and_create_bridge_table(self):
        """
        Creates bridge table and checks it columns are correct, values more one 1 row
        :return: None
        """
        list_column_table = Table(
                                name='genres_table_test',
                                columns=(Column(f'{GENRE}_id'), GENRE_COLUMN),
                                csv_file_name=self.file_name,
                                primary_key=Column(f'{GENRE}_id'),
                            )
        columns = [column.name for column in list_column_table.columns]

        file_management = FileManagement(table=list_column_table)
        file_management.create_table_with_list_in_one_cell()

        data = self.file_management.read_data_using_pandas_framework(table_name=list_column_table.name)
        columns_db = list(data.columns)
        rows, _ = data.shape

        self.assertEqual(columns, columns_db)
        self.assertGreater(rows, 1)

        # Checks if all values is unique
        values_in_column = list(data['genres'])
        self.assertEqual(len(values_in_column), len(set(values_in_column)))

        file_management.create_bridge_table()
        data = self.file_management.read_data_using_pandas_framework(table_name=f'{list_column_table.name}_titles')
        columns_db = list(data.columns)
        rows, _ = data.shape

        columns = ['genres_id', 'film_id', 'index']
        self.assertEqual(columns, columns_db)
        self.assertGreater(rows, 1)

        self.file_management.drop_table([f'{list_column_table.name}_titles', list_column_table.name])

    def test_create_table_with_one_column(self):
        """
        Creates table and checks it columns are correct, values more one 1 row
        :return: None
        """
        best_shows_by_year = Table(
            name='test_show',
            csv_file_name='Best Show by Year Netflix.csv',
            columns=(TITLE_COLUMN,),
            primary_key=FILM_ID_COLUMN
        )
        file_management = FileManagement(table=best_shows_by_year)
        file_management.main_file_name = 'raw_titles_tests.csv'
        file_management.create_table_with_one_column()

        data = self.file_management.read_data_using_pandas_framework(table_name='test_show')
        rows, columns = data.shape
        self.assertGreater(rows, 1)
        self.assertEqual(columns, 1)
        self.file_management.drop_table(['test_show'])

    def test_run_sql_query(self):
        """
        Sending sql query to DB and checking if data is changed
        :return: None
        """

        db = DBManagement()

        sql_query = """
        UPDATE movies
        SET type = 'SHOW_TEST'
        WHERE film_id like 'ts300399';
        """

        db.run_sql_query(sql_query=sql_query)

        sql_select_query = """
        select * from movies
        where film_id like 'ts300399';
        """

        values = db.run_sql_query(sql_query=sql_select_query, need_results=True)
        self.assertEqual(values[0][2], 'SHOW_TEST')

        sql_query = """
        UPDATE movies
        SET type = 'SHOW'
        WHERE film_id like 'ts300399';
        """

        db.run_sql_query(sql_query=sql_query)

        values = db.run_sql_query(sql_query=sql_select_query, need_results=True)
        self.assertEqual(values[0][2], 'SHOW')
