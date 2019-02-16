#!/usr/bin/env python
from flask import Flask, flash, redirect, render_template, request, url_for, Response
from flask import jsonify
import pymysql
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import random
import io
import base64


app = Flask(__name__)

### TO EDIT ###
sql_host = '35.197.176.134' 
sql_connection_name='lexical-archery-231806:australia-southeast1:googlecloudsql'
sql_port = 3306
sql_database = 'currencies'
sql_user = 'root'
sql_password = 'griffith_cloud_learning'
### END TO EDIT ###

### SHARED SQL FUNCTIONS ###
def sqlConnect():
    global db
    global cursor
    ##local
    db = pymysql.connect(host=sql_host, port=sql_port, database=sql_database, user=sql_user, password=sql_password) 
    ##production
    #db = pymysql.connect(unix_socket='/cloudsql/' +sql_connection_name, port=sql_port, database=sql_database, user=sql_user, password=sql_password) 
    cursor = db.cursor()
    return db
def sqlClose():
    db.close()
    return
### END SHARED SQL FUNCTIONS ###


def create_figure():
    sqlConnect()
    sql = "SELECT Symbol, SUM(Volume) as Volume FROM currencies GROUP BY Symbol "
    cursor.execute(sql)
    results = list(cursor.fetchall())
    sqlClose()
    results.sort(key=lambda x: x[1], reverse=True)

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    bar_width = 0.35
    opacity = 0.4
    values =[]
    curriencies = []
    for item in results[:5]:
        values.append(item[1])
        curriencies.append(item[0])
    axis.bar(curriencies, values, bar_width, alpha=opacity, color='b')
    return fig

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/data.json')
def getData():
    sqlConnect()
    sql = "SELECT * FROM currencies WHERE Symbol ='BTC'"
    cursor.execute(sql)
    results = list(cursor.fetchall())
    sqlClose()
    return jsonify(results)

@app.route('/')
def index():
    return render_template('index.html')
        
if __name__=='__main__':
    app.run(debug=True)