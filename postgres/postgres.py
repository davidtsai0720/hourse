# -*- coding: utf-8 -*-
import textwrap

import psycopg2

host = "localhost"
dbname = "db"
user = "postgres"
password = "postgres"
sslmode = "disable"
conn_string = f"host={host} user={user} dbname={dbname} password={password} sslmode={sslmode}"

update_syntax = textwrap.dedent('''
UPDATE hourse
SET commit = %s, updated_at = CURRENT_TIMESTAMP
WHERE link = %s;
''')


class Postgres:

    @staticmethod
    def execute(syntax: str, param: list):
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute(syntax, (*param,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def fetchone(syntax: str, param: list):
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute(syntax, (*param,))
        record = cursor.fetchone()
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def fetchall(syntax: str, param: list):
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute(syntax)
        record = cursor.fetchall()
        cursor.close()
        conn.close()
        return record
