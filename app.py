# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import pandas

from parse import parse


app = Flask(__name__)

rows = parse.Parse.filter(parse.Parse.fetch_all('output'))
default_value = pandas.DataFrame(rows).sort_values(by=['section', 'age', 'main_area', 'price'])
default_keys = tuple(default_value)
default_city = '台北市'


@app.route("/filter")
def filter():
    main_area = request.args.get('main_area')
    section = request.args.get('section')
    price = request.args.get('price')
    city = request.args.get('city')
    age = request.args.get('age')
    candidate = []

    for row in rows:

        if city and city not in row['section']:
            continue

        if section and section not in row['section']:
            continue

        if main_area and row['main_area'] < float(main_area):
            continue

        if price and row['price'] >= float(price):
            continue

        if age and float(row['age'][:-1]) >= float(age):
            continue

        if row['shape'] == '公寓' and row['floor'] != '3':
            continue

        if row['shape'] == '工廠':
            continue

        candidate.append(row)

    if len(candidate) == 0:
        return render_template(
            'index.html', data=candidate, main_area=main_area,
            section=section, price=price, city=city, age=age)

    df = pandas.DataFrame(candidate).sort_values(by=['section', 'age', 'main_area', 'price'])
    data = []
    for value in df.values.tolist():
        data.append(dict(zip(tuple(df), value)))

    return render_template(
        'index.html', data=data, main_area=main_area,
        section=section, price=price, city=city, age=age)


@app.route("/")
def index():
    data = []
    for value in default_value.values.tolist():
        data.append(dict(zip(default_keys, value)))
    return render_template('index.html', data=data, main_area='', city=default_city, price='', section='', age='')
