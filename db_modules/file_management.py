"""
This file is using to prepare data for DB. The main library - Pandas
"""
import re

import pandas as pd

from constants.columns_names_DB import FILM_ID
from constants.db_csv_data import Table
from constants.files_names import raw_titles
from constants.foreign_keys import ForeignKey
from .db_management_pandas import DBManagement


class FileManagement(DBManagement):
    """
    Data manipulation with pandas.
    """

    def __init__(self, table: Table):
        self.table: Table = table
        self.raw_data: pd.DataFrame = pd.read_csv(self.table.csv_file_name)
        self.raw_data.drop_duplicates(inplace=True)
        self.main_file_name = raw_titles
        super().__init__()

    def read_csv_file_data(self):
        print(self.raw_data.info())
        print(self.raw_data.head())

    def create_table_with_selected_columns(self, drop: bool = True) -> None:
        """
        Creates table with multiply table columns
        :return: None
        """
        columns = [column.name for column in self.table.columns]
        data = self.raw_data[columns]
        data.drop_duplicates(inplace=True)
        if drop:
            data.dropna(inplace=True)
        if isinstance(self.table.primary_key, tuple):
            primary_key = str([pk.name for pk in self.table.primary_key])[1:-1].replace("'", '"')
        else:
            primary_key = self.table.primary_key.name
        self.create_data_table_from_pandas_framework(table_name=self.table.name, data=data,
                                                     index_label=primary_key, index=False)

    def create_table_with_list_in_one_cell(self) -> None:
        """
        Created table with list format value in column
        :return: None
        """
        # self.read_csv_file_data()

        column_data = self.raw_data[self.table.columns[1].name]
        unique_values = set()
        for data in column_data:
            data = list(re.sub("['\[\]]", "", data).split(', '))
            if isinstance(data, list):
                unique_values.update(data)
            else:
                raise TypeError(f'Value {data} is not list')
        if self.table.columns[1].data_type == 'int':
            value: str
            unique_values = [int(value) for value in unique_values]
        pandas_table = pd.DataFrame(unique_values, columns=[self.table.columns[1].name])

        self.create_data_table_from_pandas_framework(table_name=self.table.name, data=pandas_table,
                                                     index_label=self.table.columns[0].name)

    def create_bridge_table(self) -> None:
        """
        Creates bridge table
        :return: None
        """
        # Extracts data from cv_file
        table_values = self.raw_data[[self.table.columns[1].name, FILM_ID]]
        data_from_csv = []
        for row in table_values.iterrows():
            cell_value = getattr(row[1], self.table.columns[1].name)
            if cell_value != cell_value:
                continue
            cell_value = list(re.sub("['\[\]]", "", cell_value).split(', '))
            for key, value in enumerate(cell_value, start=1):
                data_from_csv.append((row[1].film_id, value, key))

        book_attr = pd.DataFrame(data=data_from_csv, columns=[FILM_ID, self.table.columns[1].name, 'index'])

        # # Extracts data from DB (needs ID of attribute
        data_from_db = self.read_data_using_pandas_framework(self.table.name)

        # # Merging db and csv tables
        merge_on = self.table.columns[1].name
        merged_table = pd.merge(data_from_db, book_attr, on=merge_on)
        merged_table = merged_table.drop(columns=merge_on)

        # Creating new db table.
        primary_key_columns = str(list(merged_table.columns))[1:-1].replace("'", '"')

        self.create_data_table_from_pandas_framework(table_name=f'{self.table.name}_titles', data=merged_table,
                                                     index=False, index_label=primary_key_columns)
        self.add_foreign_key_in_table(table=self.table)

    def create_foreign_keys(self, tables: list[str, ...]):
        """
        Create references with movies table
        :param tables:
        :return: None
        """
        for table in tables:
            sql_query = f"""
            ALTER TABLE {table} ADD CONSTRAINT {table}_film_FK
            FOREIGN KEY ({self.table.primary_key.name}) REFERENCES {self.table.name}({self.table.primary_key.name});
            """
            self.run_sql_query(sql_query=sql_query)

    def create_table_with_one_column(self) -> None:
        """
        Creates table with multiply table columns
        :return: None
        """
        columns = [column.name for column in self.table.columns]
        data = self.raw_data[columns]
        data.drop_duplicates(inplace=True)
        data.dropna(inplace=True)

        main_file_columns = [self.table.primary_key.name] + columns
        main_file_data = pd.read_csv(self.main_file_name)
        main_file_data = main_file_data[main_file_columns]

        new_data = pd.merge(data, main_file_data, on=columns)
        new_data.drop(columns=columns, inplace=True)

        primary_key_column = self.table.primary_key.name
        self.create_data_table_from_pandas_framework(table_name=self.table.name, data=new_data,
                                                     index=False, index_label=primary_key_column)

    @staticmethod
    def create_foreign_key(data: ForeignKey):
        """
        Creates references between tables
        :param data:
        :return: None
        """

        sql_query = f"""
        ALTER TABLE {data.child_table_name} ADD CONSTRAINT {data.child_table_name}_{data.parent_table_name}_FK
        FOREIGN KEY ({data.key_column}) REFERENCES {data.parent_table_name}({data.key_column});
        """

        DBManagement().run_sql_query(sql_query=sql_query)
