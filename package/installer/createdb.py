import sqlite3
from sqlite3 import Error
import pathlib
from pathlib import Path

def create_connection():
    connection = pathlib.Path.cwd().parent
    try:
        connection = sqlite3.connect(f'{pathlib.Path.cwd().parent}/db.sqlite')
        print("Connection to SQLite DB successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
        connection.close()
    except Error as e:
        print(f"The error '{e}' occurred")
        connection.close()

def reading(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM users_keys")
        print(cursor.fetchall())
        print("Reading executed successfully")
        connection.close()
    except Error as e:
        print(f"The error '{e}' occurred")
        connection.close()

def return_chromedriver(connection):
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT name FROM users_keys')
        x = cursor.fetchone()
        print("Return executed successfully")
        connection.close()
        return x
    except Error as e:
        print(f"The error '{e}' occurred")
        connection.close()
        return 'Error connection to DB'

def return_path_db(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT value FROM users_keys WHERE name = 'path_to_db'")
        x = cursor.fetchone()
        print("Return executed successfully")
        connection.close()
        if x == None:
            return ('Not','Stated')
        else:
            return x
    except Error as e:
        print(f"The error '{e}' occurred")
        connection.close()
        return 'Error connection to DB'

def return_users(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT name FROM users_names")
        x = cursor.fetchall()
        print("Return executed successfully")
        connection.close()
        if x == None:
            return ('None')
        else:
            return x
    except Error as e:
        print(f"The error '{e}' occurred")
        connection.close()
        return 'Error connection to DB'

def return_bot_password(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT value FROM users_logs WHERE name = 'bot_password'")
        x = cursor.fetchall()
        print("Return executed successfully")
        connection.close()
        if x == None:
            return ('None')
        else:
            return x
    except Error as e:
        print(f"The error '{e}' occurred")
        connection.close()
        return 'Error connection to DB'

def return_bot_api(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT value FROM users_logs WHERE name = 'api_id'")
        x = cursor.fetchall()
        print("Return executed successfully")
        connection.close()
        if x == None:
            return ('None')
        else:
            return x
    except Error as e:
        print(f"The error '{e}' occurred")
        connection.close()
        return 'Error connection to DB'

def return_bot_hash(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT value FROM users_logs WHERE name = 'api_hash'")
        x = cursor.fetchall()
        print("Return executed successfully")
        connection.close()
        if x == None:
            return ('None')
        else:
            return x
    except Error as e:
        print(f"The error '{e}' occurred")
        connection.close()
        return 'Error connection to DB'

def return_bot_name(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT value FROM users_logs WHERE name = 'bot_name'")
        x = cursor.fetchall()
        print("Return executed successfully")
        connection.close()
        if x == None:
            return ('None')
        else:
            return x
    except Error as e:
        print(f"The error '{e}' occurred")
        connection.close()
        return 'Error connection to DB'

def return_bot_token(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT value FROM users_logs WHERE name = 'bot_token'")
        x = cursor.fetchall()
        print("Return executed successfully")
        connection.close()
        if x == None:
            return ('None')
        else:
            return x
    except Error as e:
        print(f"The error '{e}' occurred")
        connection.close()
        return 'Error connection to DB'


create_users_keys_table = """
CREATE TABLE IF NOT EXISTS users_keys (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  value TEXT NOT NULL
);
"""
create_users_logs_table = """
CREATE TABLE IF NOT EXISTS users_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
  value TEXT NOT NULL
);
"""
create_users_names_table = """
CREATE TABLE IF NOT EXISTS users_names (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);
"""
#
# x = create_connection()
# execute_query(x, create_users_keys_table)
# reading(create_connection())
print(return_path_db(create_connection())[0])
execute_query(create_connection(), create_users_names_table)