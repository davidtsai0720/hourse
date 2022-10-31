# -*- coding: utf-8 -*-
import textwrap

import psycopg2

host = "localhost"
dbname = "db"
user = "postgres"
password = "postgres"
sslmode = "disable"
conn_string = f"host={host} user={user} dbname={dbname} password={password} sslmode={sslmode}"
insert_syntax = textwrap.dedent('''
INSERT INTO hourse (section_id, link, layout, address, price, floor, shape, age, area, main_area, raw)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (link)
DO UPDATE
SET updated_at = CURRENT_TIMESTAMP, price = EXCLUDED.price;
''')

update_syntax = textwrap.dedent('''
UPDATE hourse
SET commit = %s, updated_at = CURRENT_TIMESTAMP
WHERE link = %s;
''')


class Postgres:

    @staticmethod
    def conn():
        return psycopg2.connect(conn_string)

    @staticmethod
    def close(conn):
        conn.close()

    @staticmethod
    def insert(conn, param: list):
        with conn.cursor() as cursor:
            cursor.execute(insert_syntax, (*param,))
            conn.commit()

    @staticmethod
    def update_commit(conn, commit: str, link: str):
        with conn.cursor() as cursor:
            cursor.execute(update_syntax, (commit, link))
            conn.commit()
