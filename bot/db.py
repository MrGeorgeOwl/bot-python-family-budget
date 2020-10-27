import os
import pdb
import pathlib
from typing import Dict, List

import psycopg2

conn = psycopg2.connect(
    host='localhost',
    dbname=os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASS'))
cursor = conn.cursor()


def insert(table: str, column_values: Dict) -> None:
    columns = ', '.join( column_values.keys() )
    values = tuple(column_values.values())
    cursor.execute(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES {values}")
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Dict]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(row):
            dict_row[columns[index]] = column
        result.append(dict_row)

    return result


def delete(table: str, row_id: int) -> None:
    cursor.execute(f"DELETE FROM {table} WHERE id={row_id}")
    conn.commit()


def get_cursor():
    return cursor


def _init_db() -> None:
    with open("bot/createdb.sql", "r") as file:
        sql = file.read()
    cursor.execute(sql)
    conn.commit()


def check_table_exist() -> None:
    cursor.execute("select exists "
                   "(select * from information_schema.tables "
                   "where table_name = 'expense');")
    table_exists = cursor.fetchall()[0][0]
    if not table_exists:
        _init_db()
    return


check_table_exist()