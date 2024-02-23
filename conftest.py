import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory
from src.main import SQLiteWriter, CSVWriter

import pytest


@pytest.fixture()
def csv_writer():
    with TemporaryDirectory() as file_dir:
        file_path = Path(file_dir) / 'test.csv'
        writer = CSVWriter(file_path, ['id', 'name', 'age'])
        yield writer
        del writer


@pytest.fixture(scope="session")
def db():
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir) / 'cars.db'
        db_ = SQLiteWriter(db_path, 'cars')
        yield db_
        del db_


@pytest.fixture(scope="function")
def cars_db(db):
    with sqlite3.connect(db.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cars')
        cursor.close()
        return db
