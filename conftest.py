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

@pytest.fixture()
def cars_db():
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir) / 'cars.db'
        db = SQLiteWriter(db_path, 'cars')
        yield db
        del db
