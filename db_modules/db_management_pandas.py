"""
File is used for CRUD with DB.
"""

import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError, InternalError
from constants.db_csv_data import Table
from constants.logins import ENGINE_PASSWORD


class DBManagement:
    """
    This class will be used for working with DB
    """
    def __init__(self, engine=ENGINE_PASSWORD):
        self.engine = create_engine(engine)

    def create_data_table_from_pandas_framework(self, data: DataFrame, table_name: str, index_label: str = 'id',
                                                index: bool = True) -> None:
        """
        Creates table in DB
        :param data: data, should be inserted in DB
        :param table_name: table name
        :param index_label: primary key column
        :param index: create primary key column.
        :return: None
        """
        data.to_sql(table_name, self.engine, index_label=index_label, if_exists='replace', index=index)
        with self.engine.connect() as con:
            con.execute(text(f'ALTER TABLE "{table_name}" ADD PRIMARY KEY ({index_label});'))
            con.commit()

    def read_data_using_pandas_framework(self, table_name: str, columns: list = None) -> pd.DataFrame:
        """
        Gets values from DB using Pandas functionality
        :param table_name: table's name
        :param columns: columns
        :return: None
        """
        return pd.read_sql(table_name, self.engine, columns=columns)

    def add_foreign_key_in_table(self, table: Table) -> None:
        """
        Adds foreign key in table (modifies columns of DB)
        :param table: table
        :return:
        """

        sql_statement = f"""
        ALTER TABLE {table.name}_titles ADD CONSTRAINT {table.name}_film_FK
        FOREIGN KEY ({table.columns[0].name}) REFERENCES {table.name}({table.columns[0].name});
        """

        self.engine = create_engine(ENGINE_PASSWORD)
        with self.engine.connect() as con:
            con.execute(text(sql_statement))
            con.commit()

    def drop_table(self, tables: list[str]) -> None:
        """
        Function drops TABLES from DB
        :return: None
        """
        with self.engine.connect() as con:
            for table in tables:
                sql_query = f"drop table {table};"
                try:
                    con.execute(text(sql_query))
                    con.commit()
                except (ProgrammingError, InternalError):
                    print(f"""SQL query:
                            {sql_query}
                            was not executed""")

    def run_sql_query(self, sql_query: str, need_results: bool = False):
        """
        Runs any SQL query in databases and return values if needs
        :param sql_query: sql query
        :param need_results: True if needs return values from DB.
        :return:
        """
        with self.engine.connect() as con:
            try:
                result = con.execute(text(sql_query))
                con.commit()
            except ProgrammingError:
                print(f"""
                {sql_query}
                was not executed""")
        if need_results:
            return result.fetchall()
