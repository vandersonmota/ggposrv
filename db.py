# coding: utf-8

import os
import sys
import logging

DB_ENGINE=os.environ.get('DB_ENGINE', 'sqlite3')


config = {
    'engine': DB_ENGINE,
    'param': '', 
    'user': 'ggpo', # not need for sqlite
    'passwd': 'ggpo', # not need for sqlite
    'host': 'localhost', # not need for sqlite
    'port': '', # empty for default port
    'db': '',
}


if DB_ENGINE=="sqlite3":
    import sqlite3
    config['param'] = "?"
    config['db'] = os.path.join(os.path.realpath(os.path.dirname(sys.argv[0])),'db', 'ggposrv.sqlite3')
elif DB_ENGINE=="mysql":
    import MySQLdb
    config['param']="%s"
    config['db'] = 'ggposrv'

def connect():
    dbfile = os.path.join(os.path.realpath(os.path.dirname(sys.argv[0])), 'ggposrv.sqlite3')
    if config['engine'] == 'sqlite3':
        conn = sqlite3.connect(dbfile)
    elif config['engine'] == 'mysql':
        conn = MySQLdb.connect(host=config['host'], user=config['user'], 
            passwd=config['passwd'], db=config['db'])
    return conn


def create_schema():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT COLLATE NOCASE,
                password TEXT,
                salt TEXT,
                email TEXT,
                ip TEXT,
                date TEXT);""")
    cursor.execute("""CREATE UNIQUE INDEX users_username_idx on users (username COLLATE NOCASE);""")
    logging.info("created empty user database")
    cursor.execute("""CREATE TABLE IF NOT EXISTS quarks (
                id INTEGER PRIMARY KEY,
                quark TEXT,
                player1 TEXT,
                player2 TEXT,
                channel TEXT,
                date TEXT,
                realtime_views INTEGER,
                saved_views INTEGER,
                p1_country CHAR(50),
                p2_country CHAR(50),
                duration INTEGER);""")
    cursor.execute("""CREATE UNIQUE INDEX quarks_quark_idx on quarks (quark);""")
    logging.info("created empty quark database")
    conn.commit()

if __name__ == '__main__':
    logging.info('creating schema')
    create_schema()
