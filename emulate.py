#!/usr/bin/env python

# all the imports
from __future__ import with_statement
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import StateManager

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

@app.route('/stop', methods=['POST'])
def stop():
     #Stop the automatic updates
     flash('Updates halted.')
     session['updates_paused'] = True
     global gState
     gState.Pause()
     return redirect(url_for('vehicle_data'))

@app.route('/single', methods=['POST'])
def single():
     #make a global socket
     flash('Single packet sent.')
     global gState
     gState.SingleUpdate()
     return redirect(url_for('vehicle_data'))

@app.route('/start', methods=['POST'])
def start():
     #make a global socket
     flash('Updates resumed.')
     session.pop('updates_paused', None)
     global gState
     gState.Resume()
     return redirect(url_for('vehicle_data'))

@app.route('/update', methods=['POST'])
def update_steering_wheel():
     angle = request.form['angle']
     print "New Steering Wheel Angle: " + angle
     flash('Steering Wheel Angle set to ' + angle)
     global gState
     gState.update_angle(angle)
     return redirect(url_for('vehicle_data'))

if __name__ == '__main__':
     print 'Running Main...'
     init_db()
     
     global gState
     gState = StateManager.StateManager()

     app.run(use_reloader=False)
     
