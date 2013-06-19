#!/usr/bin/env python

# all the imports
from __future__ import with_statement
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import EnablerConnection

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def vehicle_data():
    return render_template('vehicle_controls.html')

@app.route('/connect', methods=['POST'])
def connect():
     #make a global socket
     global gConn
     gConn = EnablerConnection.EnablerConnection()
     gConn.create_socket_connection('', 50013)
     return render_template('vehicle_controls.html')
#     return redirect(url_for('vehicle_data'))

@app.route('/update', methods=['POST'])
def update_steering_wheel():
     angle = request.form['angle']
     print "New Steering Wheel Angle: " + angle
     flash('Steering Wheel Angle set to ' + angle)
     gConn.send("{\"name\":\"steering_wheel_angle\",\"value\":" + angle + "}")
     return redirect(url_for('vehicle_data'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('vehicle_data'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('vehicle_data'))

if __name__ == '__main__':
     print 'Running Main...'
     init_db()
     app.run()
