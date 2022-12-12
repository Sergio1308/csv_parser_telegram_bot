from contextlib import contextmanager
from db.connection import get_connection
from psycopg2 import sql


def create_tables(table_names):
    """
    Create all tables, get their name from table_names list (parsed from CSV file as first column)

    :param table_names: list of table names (parsed from CSV file as first column)
    :return: None
    """
    for name in table_names:
        CREATE_TABLE = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {}
            (
                id SERIAL PRIMARY KEY,
                {} TEXT
            );
        """).format(sql.Identifier(name), sql.Identifier(name))
        with get_connection() as connection:
            with get_cursor(connection) as cursor:
                cursor.execute(CREATE_TABLE)


def add_new_columns(table_names, fields):
    """
    Add new values to tables.

    :param table_names: list of table names (parsed from CSV file as first column)
    :param fields: list of values from field
    :return: None
    """
    for t_name, f_name in zip(table_names, fields):
        INSERT_QUERY = sql.SQL("""INSERT INTO {} ({}) VALUES (%s);""").format(
            sql.Identifier(t_name), sql.Identifier(t_name)
        )
        with get_connection() as connection:
            with get_cursor(connection) as cursor:
                cursor.execute(INSERT_QUERY, (str(f_name),))


def set_foreign_keys(table_names):
    print(table_names[1:])
    for index, name in reversed(list(enumerate(table_names[1:]))):
        # print(name, table_names[len(table_names)-index-1])
        print(name, )
        QUERY = """
            ALTER TABLE {} ADD CONSTRAINT id FOREIGN KEY (id) REFERENCES {} (id);
        """


if __name__ == '__main__':
    set_foreign_keys(['name1', 'name2', 'name3'])


def getData():
    SELECT_QUERY = """SELECT * FROM startdate LIMIT 100"""
    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(SELECT_QUERY)
            records = cursor.fetchall()
            for row in records:
                print("Id = ", row[0], )
                print("Value = ", row[1])


@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor
