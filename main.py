import csv
import random
import sqlite3
from time import sleep

import requests
from bs4 import BeautifulSoup

from fake_user_agents import user_agents
from car_brands import brand


def random_sleep():
    sleep(random.randint(2, 5))


def get_page_content(page: int, page_size: int = 100, brand_id: int = None):

    base_url = 'https://auto.ria.com/uk/search/'
    query_params = {
        'indexName': 'auto,order_auto,newauto_search',
        'categories.main.id': '1',
        'country.import.usa.not': '-1',
        'price.currency': '1',
        'abroad.not': '0',
        'custom.not': '1',
        'page': page,
        'size': page_size,
        'brand.id[0]': brand_id,
    }

    headers = {
        'User-Agent': random.choice(user_agents)
    }

    response = requests.get(base_url, params=query_params, headers=headers)
    response.raise_for_status()
    return response.text


def get_car_info(car_link: str):
    headers = {
        'User-Agent': random.choice(user_agents)
    }

    response = requests.get(f"https://auto.ria.com{car_link}", headers=headers)
    response.raise_for_status()
    return response.text


class CSVWriter:
    def __init__(self, file_name: str, headers: list):
        self.file_name = file_name

        with open(self.file_name, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

    def write_data(self, data: dict):
        with open(self.file_name, 'a') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            writer.writerow(data)


class SQLiteWriter:
    def __init__(self, db_name: str, table_name: str):
        self.db_name = db_name
        self.table_name = table_name

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY,
                mark TEXT,
                model TEXT,
                year INTEGER,
                link TEXT,
                title TEXT,
                description TEXT)""")

    def write_data(self, data):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute(f"""SELECT * FROM {self.table_name}
                               WHERE id = ?""", (data['car_id'],))
            if cursor.fetchone():
                print(f"Record with id {data['car_id']} already exists in the database!")
            else:
                cursor.execute(f"""INSERT INTO {self.table_name} (id, mark, model, year, link, title, description)
                                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                               (
                                   data['car_id'],
                                   data['car_mark_details'],
                                   data['car_model_name'],
                                   data['car_year'],
                                   data['car_link_to_view'],
                                   data['title'],
                                   data['description']
                               ))


def main():
    page = 0
    headers = ['id', 'mark', 'model', 'year', 'link', 'title', 'description']

    writers = (
        CSVWriter('cars1.csv', headers),
        SQLiteWriter('cars.db', 'cars'),
    )

    while True:
        if page > 2:
            break
        # random_sleep()
        print(f"Processing page {page}!")

        page_content = get_page_content(page, brand_id=brand['citroen'])

        soup = BeautifulSoup(page_content, 'html.parser')
        search_results = soup.find('div', id="searchResults")
        ticket_items = search_results.find_all("section", class_="ticket-item")

        if not ticket_items:
            print(f"No more items on page {page}!")
            break

        for ticket_item in ticket_items:
            random_sleep()
            data = {}

            ticket_data = ticket_item.find("div", class_="hide")
            data['car_id'] = ticket_data['data-id']
            data['car_mark_details'] = ticket_data['data-mark-name']
            data['car_model_name'] = ticket_data['data-model-name']
            data['car_year'] = ticket_data['data-year']
            data['car_link_to_view'] = ticket_data['data-link-to-view']

            car_link = ticket_data['data-link-to-view']
            car_details = get_car_info(car_link)
            print(f"Retrieving car details for {car_link}")
            car_details_parsed = BeautifulSoup(car_details, 'html.parser')

            data['title'] = car_details_parsed.find('title').text
            data['description'] = car_details_parsed.find('meta', attrs={'name': 'description'})['content']

            for writer in writers:
                writer.write_data(data)
            print(data)

        page += 1


if __name__ == '__main__':
    main()
