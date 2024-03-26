# vipranc-DE1.4

# Introduction

This script is for ingesting data from CSV files, normalizing tables, and ingesting data to DB.

It requires Python >=3.9

# Development

## Writing source code

Consider follow:
* [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

## Installation

Create virtual environment:

    python -m venv .venv

Install package:

    pip install -r requirements.txt


# Usage

Data are prepared using two classes in files manage_csv_file.py and file_management.py files. All MetaData must be written in constants.
db_management.py file contains classes that create connections with DB.

Database ERD schema: 
![image](https://github.com/TuringCollegeSubmissions/vipranc-DE1.4/assets/68908834/e7d7a188-9ad4-4919-97bd-7e11633d8022)
