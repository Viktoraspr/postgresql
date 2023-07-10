"""
This file contains class, which creates new file with correct columns formats.
"""


import pandas as pd

class CSVFileCorrection:
    """
    Creates new file with correct columns formats.
    """
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.raw_data: pd.DataFrame = pd.read_csv(self.file_name)

    def read_data(self):
        print(self.raw_data.head())
        print(self.raw_data.info())

    def lower_column_names(self):
        """
        Lowers all column names of file
        :return: None
        """

        columns = self.raw_data.columns
        columns_lower = [column.lower() for column in columns]

        new_columns_names = {col: col_low for col, col_low in zip(columns, columns_lower)}
        self.raw_data.rename(columns=new_columns_names, inplace=True)
        self.raw_data = self.raw_data.drop_duplicates()

    def change_column_name(self, old_name, new_name):
        """
        Renames column names
        :param old_name: old column name
        :param new_name: new column name
        :return: None
        """
        columns = list(self.raw_data.columns)
        if old_name in columns:
            self.raw_data.rename(columns={old_name: new_name}, inplace=True)

    def write_new_data_to_csv_file(self):
        """
        Overwrites file with modified data
        :return: None
        """
        self.raw_data.to_csv(self.file_name, index=False)
