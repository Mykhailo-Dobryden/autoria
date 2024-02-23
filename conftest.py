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


@pytest.fixture(scope="session")
def some_cars_data():

    return [
        {
            'car_id': 1,
            'car_mark_details': 'toyota',
            'car_model_name': 'corolla',
            'car_year': 2025,
            'car_link_to_view': '/toyota-cololla-1',
            'title': 'Toyota Corolla 2020 title',
            'description': 'Toyota Corolla 2020 description',
        },
        {
            'car_id': 2,
            'car_mark_details': 'mazda',
            'car_model_name': 'cx-5',
            'car_year': 2020,
            'car_link_to_view': '/mazda-cx-5-2',
            'title': 'Mazda CX-5 2020 title',
            'description': 'Mazda CX-5 2020 description',
        },
        {
            'car_id': 3,
            'car_mark_details': 'chevrolet',
            'car_model_name': 'aveo',
            'car_year': 2014,
            'car_link_to_view': '/chevrolet-aveo-3',
            'title': 'Chevrolet Aveo 2014 title',
            'description': 'Chevrolet Aveo 2014 description',
        },
        {
            'car_id': 4,
            'car_mark_details': 'bmw',
            'car_model_name': 'x5',
            'car_year': 2021,
            'car_link_to_view': '/bmw-x5-4',
            'title': 'BMW X5 2021 title',
            'description': 'BMW X5 2021 description',
        }
    ]
