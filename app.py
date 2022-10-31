# -*- coding: utf-8 -*-
import textwrap
from flask import Flask, render_template, request
# import pandas

# from parse import parse
from postgres.postgres import Postgres


app = Flask(__name__)

# raw = parse.Parse.fetch_all('output')
# rows = parse.Parse.filter(raw)
# default_value = pandas.DataFrame(rows).sort_values(by=['section', 'age', 'main_area', 'price'])
# default_keys = tuple(default_value)
# default_city = '台北市'


@app.route("/filter")
def filter():
    main_area = request.args.get('main_area')
    section = request.args.get('section')
    price = request.args.get('price')
    city = request.args.get('city')
    age = request.args.get('age')
    return render_template('index.html')


@app.route("/")
def index():
    syntax = textwrap.dedent('''
WITH duplicate_conditions AS (
    SELECT MIN(id) AS id, section_id, address, age, area
    FROM hourse
    WHERE link LIKE 'https://sale.591.com.tw/home%'
    AND updated_at > CURRENT_TIMESTAMP - INTERVAL '1 day'
    GROUP BY section_id, address, age, area
    HAVING count(1) > 1
),
duplicate AS (
    SELECT hourse.id
    FROM hourse
    INNER JOIN duplicate_conditions ON(
            hourse.section_id = duplicate_conditions.section_id
        AND hourse.address = duplicate_conditions.address
        AND hourse.age = duplicate_conditions.age
        AND hourse.area = duplicate_conditions.area
        AND hourse.link LIKE 'https://sale.591.com.tw/home%'
    )
    WHERE hourse.id NOT IN (SELECT id FROM duplicate_conditions)
    AND hourse.updated_at > CURRENT_TIMESTAMP - INTERVAL '1 day'
    ORDER BY hourse.address, hourse.age, hourse.area
)
SELECT
    CONCAT(city.name, section.name, hourse.address) AS address,
    hourse.price,
    CONCAT(hourse.current_floor, '/', hourse.total_floor) AS floor,
    hourse.shape,
    hourse.age,
    hourse.main_area,
    hourse.area,
    section.name AS section,
    hourse.link,
    COALESCE(hourse.commit, '') AS commit
FROM hourse
LEFT JOIN section ON (section.id=hourse.section_id)
LEFT JOIN city ON (city.id=section.city_id)
WHERE hourse.updated_at > CURRENT_TIMESTAMP - INTERVAL '1 day'
AND hourse.id NOT IN (SELECT id FROM duplicate)
AND hourse.main_area IS NOT NULL
AND city.name = '台北市'
AND hourse.main_area >= 18
AND hourse.price < 2200
AND hourse.age < '40'
ORDER BY city.name, section.name, hourse.age, hourse.price, hourse.address;
''')

    results = Postgres.fetchall(syntax, [])
    keys = ('address', 'price', 'floor', 'shape', 'age', 'main_area', 'area', 'section', 'link', 'other')
    for i in range(len(results)):
        results[i] = dict(zip(keys, results[i]))
    return render_template('index.html', data=results)
