#!/usr/bin/env python
import sqlite3
from sqlite3 import Error
import os
from colorama import Fore, init
init(autoreset=True)

path = os.path.abspath(os.curdir)

def sql_connection(method):
    def wrapper(*args, **kwargs):
        try:
            kwargs['connect'] = sqlite3.connect(f'{path}/account.db')
            result = method(*args, **kwargs)
            print('✅')
            return result
        except Error as error:
            print('❌')
            print(Fore.RED + f'ERROR: {error}')
        finally:
            kwargs['connect'].close()
    return wrapper

#create tables
def make_tables():
    @sql_connection
    def accounts(connect):
        cursor = connect.cursor()
        print(Fore.BLUE + f'TABLE: accounts', end=" ")
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS accounts(
        PHONE TEXT PRIMARY KEY,
        API_ID INTEGER,
        API_HASH TEXT,
        APP_VERSION TEXT,
        DEVICE_MODEL TEXT,
        SYSTEM_VERSION TEXT,
        WALLET TEXT)""")
        connect.commit()
    accounts()

    @sql_connection
    def chanels(connect):
        cursor = connect.cursor()
        print(Fore.BLUE + f'TABLE: chanels', end=" ")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chanels(
        ID INTEGER PRIMARY KEY,
        PHONE TEXT,
        CHANEL_ID INTEGER NOT NULL,
        TIMER INTEGER NOT NULL)""")
        connect.commit()
    chanels()

#view tables
@sql_connection
def view_all_tables(connect):
    cursor = connect.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    result = cursor.fetchall()
    for row in result:
        print(*row)
    connect.commit()
#удаление таблицы
@sql_connection
def remove_table(table, connect):
    print(Fore.YELLOW + f'DELETE {table}', end=" ")
    cursor = connect.cursor()
    cursor.execute(f'DROP TABLE IF EXISTS {table}')
    print(Fore.YELLOW + f'DELETE TABLE: {table}', end=" ")
    connect.commit()
#read all in table
@sql_connection
def table_read_all(table, connect):
    cursor = connect.cursor()
    cursor.execute(f'SELECT * FROM {table}')
    rows = cursor.fetchall()
    for row in rows:
        print(*row)
#read row in table
@sql_connection
def table_read_row(table, row, connect):
    cursor = connect.cursor()
    cursor.execute(f'SELECT {row} FROM {table}')
    rows = cursor.fetchall()
    result = set()
    for row in rows:
        result.add(row[0])
    connect.commit()
    print(result, end=" ")
    return result

#insert account
@sql_connection
def account_insert(phone, api_id, api_hash, app_version, device_model, system_version, wallet, connect):
    print(Fore.BLUE + f'{phone} add in DB', end=" ")
    cursor = connect.cursor()
    cursor.execute(
        f'INSERT INTO accounts(PHONE, API_ID, API_HASH, APP_VERSION, DEVICE_MODEL, SYSTEM_VERSION, WALLET) '
        f'VALUES(?,?,?,?,?,?,?)',
        (phone, api_id, api_hash, app_version, device_model, system_version, wallet))
    connect.commit()
#delete account
@sql_connection
def account_delete(phone, connect):
    print(Fore.YELLOW + f'{phone} DELETE FROM DB', end=" ")
    cursor = connect.cursor()
    cursor.execute(f'DELETE FROM accounts WHERE PHONE = "{phone}"')
    connect.commit()
#insert chanel
@sql_connection
def chanel_insert(phone, chanel_id, timer, connect):
    print(Fore.BLUE + f'{phone} add in DB', end=" ")
    cursor = connect.cursor()
    cursor.execute(
        f'INSERT INTO chanels(PHONE, CHANEL_ID, TIMER) '
        f'VALUES(?,?,?)',
        (phone, chanel_id, timer))
    connect.commit()
#upgrade chanel
@sql_connection
def chanel_upgrade(phone, chanel_id, timer, connect):
    print(Fore.BLUE + f'{phone} add in DB', end=" ")
    cursor = connect.cursor()
    cursor.execute(f'UPDATE chanels SET TIMER = {timer} WHERE PHONE = "{phone}" AND CHANEL_ID = "{chanel_id}"')
    connect.commit()


#--------  CHANEL TABLE  --------#

@sql_connection
def get_id_key(phone, connect):
    cursor = connect.cursor()
    cursor.execute(f'SELECT ID FROM chanels WHERE PHONE = "{phone}"')
    rows = cursor.fetchall()
    result = set()
    for row in rows:
        result.add(row[0])
    connect.commit()
    return result

@sql_connection
def get_timer(id, connect):
    cursor = connect.cursor()
    cursor.execute(f'SELECT TIMER FROM chanels WHERE ID = "{id}"')
    rows = cursor.fetchall()
    for row in rows:
        return row[0]
    connect.commit()

@sql_connection
def get_chanel_id(id, connect):
    cursor = connect.cursor()
    cursor.execute(f'SELECT CHANEL_ID FROM chanels WHERE ID = "{id}"')
    rows = cursor.fetchall()
    for row in rows:
        return row[0]
    connect.commit()

@sql_connection
def chanel_delete(id, phone, chanel_id, connect):
    print(Fore.YELLOW + f'{phone} DELETE: {chanel_id}', end=" ")
    cursor = connect.cursor()
    cursor.execute(f'DELETE FROM chanels WHERE ID = "{id}"')
    connect.commit()

#--------  ACOUNTS TABLE  --------#

@sql_connection
def get_api_id(phone, connect):
    cursor = connect.cursor()
    cursor.execute(f'SELECT API_ID FROM accounts WHERE PHONE = "{phone}"')
    rows = cursor.fetchall()
    for row in rows:
        print(row[0], end=" ")
        return row[0]
    connect.commit()

@sql_connection
def get_api_hash(phone, connect):
    cursor = connect.cursor()
    cursor.execute(f'SELECT API_HASH FROM accounts WHERE PHONE = "{phone}"')
    rows = cursor.fetchall()
    for row in rows:
        print(row[0], end=" ")
        return row[0]
    connect.commit()

@sql_connection
def get_app_version(phone, connect):
    cursor = connect.cursor()
    cursor.execute(f'SELECT APP_VERSION FROM accounts WHERE PHONE = "{phone}"')
    rows = cursor.fetchall()
    for row in rows:
        print(row[0], end=" ")
        return row[0]
    connect.commit()

@sql_connection
def get_device_model(phone, connect):
    cursor = connect.cursor()
    cursor.execute(f'SELECT DEVICE_MODEL FROM accounts WHERE PHONE = "{phone}"')
    rows = cursor.fetchall()
    for row in rows:
        print(row[0], end=" ")
        return row[0]
    connect.commit()

@sql_connection
def get_system_version(phone, connect):
    cursor = connect.cursor()
    cursor.execute(f'SELECT SYSTEM_VERSION FROM accounts WHERE PHONE = "{phone}"')
    rows = cursor.fetchall()
    for row in rows:
        print(row[0], end=" ")
        return row[0]
    connect.commit()

@sql_connection
def get_wallet(phone, connect):
    cursor = connect.cursor()
    cursor.execute(f'SELECT WALLET FROM accounts WHERE PHONE = "{phone}"')
    rows = cursor.fetchall()
    for row in rows:
        print(row[0], end=" ")
        return row[0]
    connect.commit()

#table_read_all(table='chanels')