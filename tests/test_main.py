import sqlite3

from src.main import SQLiteWriter, CSVWriter


def test_CSWWriter(csv_writer):
    writer = CSVWriter(csv_writer.file_name, ['id', 'name', 'age'])
    writer.write_data({'id': 1, 'name': 'John', 'age': 25})
    assert csv_writer.file_name.read_text() == 'id,name,age\n1,John,25\n'



def test_empty(cars_db):
    conn = sqlite3.connect(cars_db.db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cars')
    assert cursor.fetchall() == []


