import sqlite3


# --- CLASSES ---

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._instance._initialise()
        return cls._instance

    def _initialise(self):
        self.connection = sqlite3.connect('db.db')

class Observer:
    def __init__(self, name: str) -> None:
        self.name = name

    def update(self, message: str) -> None:
        print(f"Received: {message}")

db1 = DatabaseConnection()
db2 = DatabaseConnection()

print(db1 == db2)

# --- DATABASE FUNCTIONS ---


# --- TABLE FUNCTIONS ---

def create_table(connection,
                table_name: str,
                table_columns: list):
    """
    ...Creates a table inside the database.

    Parameters:
        connection: The database connection.
        table_name (STR): The name of the table to be created.
        table_columns (LIST): The columns to be added to the table.
    """
    c = connection.cursor()
    query = ("CREATE TABLE IF NOT EXISTS {} ({})").format(table_name, ", ".join(table_columns))
    c.execute(query)
    connection.commit()

def read_table(connection, table_name: str):
    """
    ...Returns all data from a specific table.

    Parameters:
        connection: The database connection.
        table_name (STR): The name of the table to read data from.
    """
    c = connection.cursor()
    c.execute("SELECT * FROM {}").format(table_name)
    return c.fetchall()

def update_table_insert(connection,
                        table_name: str,
                        table_columns: list,
                        table_data: list):
    """
    ...Inserts data into a row within a table.

    Parameters:
        connection: The database connection.
        table_name (STR): The name of the table to be updated.
        table_columns (LIST): The columns to be updated.
        table_data (LIST): The data to be inserted into the table.
    """
    c = connection.cursor()
    columns = ", ".join(table_columns)
    data_placeholder = ", ".join("?") * len(table_data)

    query = f"INSERT INTO {table_name} ({columns}) VALUES ({data_placeholder})"
    c.execute(query, table_data)

    return


### - COLUMN FUNCTIONS ---

def create_column(connection,
                  table_name: str,
                  column_name: str,
                  column_modifiers: list):
    """
    ...Adds a column to an already existing table.

    Parameters:
        connection: The database connection.
        table_name (STR): The name of the table to be altered.
        column_name (STR): The name of the new column to be inserted.
        column_modifiers (LIST): (optional) The modifiers that define the data types and rules for the new column.
    """
    c = connection.cursor()

    if column_modifiers:
        query = ("ALTER TABLE {} ADD {} ({})").format(table_name, column_name, ", ".join(column_modifiers))
    else:
        query = ("ALTER TABLE {} ADD {}").format(table_name, column_name)

    c.execute(query)
    connection.commit()


# --- SETUP AND INITIALISATION ---

db = DatabaseConnection()

create_table(db.connection, "Films", ["id INTEGER PRIMARY KEY AUTOINCREMENT", "film_name TEXT", "film_description TEXT", "film_cast TEXT"])