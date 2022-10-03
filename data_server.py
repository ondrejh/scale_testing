#!/usr/bin/python3

from flask import Flask, render_template
from flask_json import FlaskJSON, JsonError, json_response, as_json
import datetime

import random
random.seed()

from data_thread import data_thread
from filter import filter

app = Flask(__name__)
FlaskJSON(app)

data = {}
filters = {}
cnts = {}

@app.route('/')
@app.route('/home')
def home():
    """ Renders the home page. """
    #return render_template('index.html')
    return "Hello world!"

@app.route('/data.json')
@as_json
def get_data():
    """ Render json data. """
    data['value'] = random.randint(0, 10000)
    return data

def data_in(sid, svalue):
    strid = str(sid)
    if strid not in data.keys():
        data[strid] = {}
        data[strid]['short'] = {'val': [], 'avg': [], 'med': [], 'min': [], 'max': []}
        filters[strid] = filter()
        cnts[strid] = 0
    if cnts[strid] == 0:
        data[strid]['val'] = svalue
        davg, dmed, dmin, dmax = filters[strid].put(svalue)
        data[strid]['avg'] = davg
        data[strid]['med'] = dmed
        data[strid]['min'] = dmin
        data[strid]['max'] = dmax
        tstamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        for k in ('val', 'avg', 'med', 'min', 'max'):
            dt = data[strid]['short'][k]
            val = data[strid][k]
            if len(dt) < 1 or dt[-1][1] != val:
                dt.append([tstamp, val])
            if len(dt) > 100:
                data[strid]['short'][k] = dt[-100:]

    cnts[strid] += 1
    if cnts[strid] >= 10:
        cnts[strid] = 0

if __name__ == '__main__':

    dtt = data_thread(fout=data_in)
    dtt.start()

    app.run()
