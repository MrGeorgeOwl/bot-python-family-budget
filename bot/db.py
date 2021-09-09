"""Module which contains functions for working with db."""
import os
from typing import List

from psycopg2 import connect, sql

conn = connect(
    host=os.environ.get('HOST', 'localhost'),
    dbname=os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASS'),
)
cursor = conn.cursor()


def insert(table: str, column_values: dict) -> None:
    """
    Insert new row in table.

    Args:
        table: Table name.
        column_values: Values of new row.
    """
    query = sql.SQL(
        'INSERT INTO {table} '
        + '({columns}) ',
    ).format(
        table=sql.Identifier(table),
        columns=sql.SQL(',').join(
            [sql.Identifier(key) for key in column_values.keys()],
        ),
        row_values=sql.SQL(',').join(
            [sql.Literal(row_value) for row_value in column_values.values()],
        ),
    )
    cursor.execute(query)
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[dict]:
    """
    Fetch all columns from table.

    Args:
        table: Table name.
        columns: Columns of table which must be returned.

    Returns:
        List of rows.
    """
    query = sql.SQL(
        'SELECT {columns} FROM {table}',
    ).format(
        columns=sql.SQL(',').join(
            [sql.Identifier(column) for column in columns],
        ),
        table=sql.Identifier(table),
    )
    cursor.execute(query)
    rows = cursor.fetchall()

    return [
        {
            columns[index]: column_value
            for index, column_value in enumerate(row)
        }
        for row in rows
    ]


def delete(table: str, row_id: int) -> None:
    """
    Delete table row.

    Args:
        table: Table name.
        row_id: Id of row which must be deleted.
    """
    query = sql.SQL(
        'DELETE FROM {table} WHERE id={row_id}',
    ).format(
        table=sql.Identifier(table),
        row_id=sql.Literal(row_id),
    )
    cursor.execute(query)
    conn.commit()


def get_cursor():
    """
    Get cursor connection with db.

    Returns:
        Cursor object to connect with db.
    """
    return cursor


def _init_db() -> None:
    with open('bot/createdb.sql', 'r') as sql_script:
        sql_content = sql_script.read()
    cursor.execute(sql_content)
    conn.commit()


def check_table_exist() -> None:
    """Check table existence and create it if needed."""
    query = sql.SQL(
        'SELECT EXISTS '
        + '(SELECT * FROM {from_table} '  # noqa: S608
        + 'WHERE table_name = {table});',
    ).format(
        from_table=sql.Identifier('information_schema.tables'),
        table=sql.Identifier('expense'),
    )
    cursor.execute(
        query,
    )
    table_exists = cursor.fetchall()[0][0]
    if not table_exists:
        _init_db()


check_table_exist()
