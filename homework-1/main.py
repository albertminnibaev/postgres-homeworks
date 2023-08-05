"""Скрипт для заполнения данными таблиц в БД Postgres."""

import psycopg2
import csv
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

# переменные для хранения адреса к файлам с данными
customers_data_csv = os.path.join("north_data", "customers_data.csv")
employees_data_csv = os.path.join("north_data", "employees_data.csv")
orders_data_csv = os.path.join("north_data", "orders_data.csv")


def get_data(file):
    """
    Функция для чтения информации из файлов csv
    :param file: файл csv с данными
    :return: список кортежей, где котеж - это строка из файла csv (без строки заголовка)
    """
    with open(file, encoding="utf-8") as file_csv:
        file_reader = csv.reader(file_csv, delimiter = ",")
        file_list = []
        for i in file_reader:
            file_list.append(tuple(i))
        return file_list[1:]


if __name__ == "__main__":
    #with psycopg2.connect(host="localhost", database="north", user="postgres", password="albert") as conn:
    with psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD) as conn:
        with conn.cursor() as cur:
            for i in get_data(employees_data_csv):
                cur.execute(f"INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)", i)
            for i in get_data(customers_data_csv):
                cur.execute(f"INSERT INTO customers VALUES (%s, %s, %s)", i)
            for i in get_data(orders_data_csv):
                cur.execute(f"INSERT INTO orders VALUES (%s, %s, %s, %s, %s)", i)
    conn.close()
