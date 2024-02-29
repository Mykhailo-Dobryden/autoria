import sqlite3

from src.main import SQLiteWriter, CSVWriter


def test_CSWWriter(csv_writer):
    writer = CSVWriter(csv_writer.file_name, ['id', 'name', 'age'])
    writer.write_data({'id': 1, 'name': 'John', 'age': 25})
    assert csv_writer.file_name.read_text() == 'id,name,age\n1,John,25\n'


def test_sqlitewriter_write_data(cars_db):
    data = {
        'car_id': 1,
        'car_mark_details': 'toyota',
        'car_model_name': 'corolla',
        'car_year': 2020,
        'car_link_to_view': '/toyota-cololla-1',
        'title': 'Toyota Corolla 2020 title',
        'description': 'Toyota Corolla 2020 description',
    }
    cars_db.write_data(data)
    conn = sqlite3.connect(cars_db.db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cars')
    assert cursor.fetchall() == [(1, 'toyota', 'corolla', 2020, '/toyota-cololla-1',
                                  'Toyota Corolla 2020 title', 'Toyota Corolla 2020 description')]
    cursor.close()


def test_sqlitewriter_write_data_already_exists(cars_db, capsys, some_cars_data):
    data = {
        'car_id': 1,
        'car_mark_details': 'toyota',
        'car_model_name': 'corolla',
        'car_year': 2020,
        'car_link_to_view': '/toyota-cololla-1',
        'title': 'Toyota Corolla 2020 title',
        'description': 'Toyota Corolla 2020 description',
    }

    for d in some_cars_data:
        cars_db.write_data(d)

    cars_db.write_data(data)
    out = capsys.readouterr().out
    assert out == f"Record with id {data['car_id']} already exists in the database!\n"


def test_empty(cars_db):
    conn = sqlite3.connect(cars_db.db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cars')
    # breakpoint()
    assert cursor.fetchall() == []
