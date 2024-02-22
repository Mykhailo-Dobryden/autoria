import sqlite3

from src.main import SQLiteWriter, CSVWriter


def test_CSWWriter():
    writer = CSVWriter('test.csv', ['id', 'name', 'age'])
    writer.write_data({'id': 1, 'name': 'John', 'age': 25})

    with open('test.csv', 'r') as f:
        assert f.read() == 'id,name,age\n1,John,25\n'


def test_SQLiteWriter_valid_data():
    writer = SQLiteWriter('test.db', 'test_table')
    writer.write_data(
        {
            'car_id': 1,
            'car_mark_details': 'BMW',
            'car_model_name': 'X5',
            'car_year': 2020,
            'car_link_to_view': '/link_1',
            'title': 'BMW X5 2020',
            'description': 'Some description'
        }
    )

    with sqlite3.connect('test.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM test_table')
        assert cursor.fetchone() == (1, 'BMW', 'X5', 2020, '/link_1', 'BMW X5 2020', 'Some description')