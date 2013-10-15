#!/usr/bin/env python

# all the imports

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
        render_template, flash, jsonify, make_response
from contextlib import closing
import state_manager

# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def _make_status_response(status):
    response = make_response()
    response.status_code = status
    return response

@app.route('/')
def vehicle_data():
     global gState
     return render_template('vehicle_controls.html', IP=gState.local_ip,
             accelerator=gState.accelerator_pedal_position,
             angle=gState.steering_wheel_angle)

@app.route('/stop', methods=['POST'])
def stop():
     #Stop the automatic updates
     session['updates_paused'] = True
     global gState
     gState.pause()
     return redirect(url_for('vehicle_data'))

@app.route('/single', methods=['POST'])
def single():
     #make a global socket
     global gState
     gState.update_once()
     return redirect(url_for('vehicle_data'))

@app.route('/start', methods=['POST'])
def start():
     #make a global socket
     session.pop('updates_paused', None)
     global gState
     gState.resume()
     return redirect(url_for('vehicle_data'))

@app.route('/_set_data', methods=['POST'])
def set_data():
     global gState

     name = request.form['name']

     if name == "angle":
          gState.steering_wheel_angle = float(request.form['value'])
     elif name == "accelerator":
          gState.accelerator_pedal_position = float(request.form['value'])
     elif name == "brake":
          gState.brake_pedal_position = float(request.form['value'])
     elif name == "parking_brake_status":
          gState.parking_brake_status = python_bool(request.form['value'])
     elif name == "ignition_status":
          gState.ignition_status = request.form['value']
     elif name == "headlamp_status":
          gState.headlamp_status = python_bool(request.form['value'])
     elif name == "high_beam_status":
          gState.high_beam_status = python_bool(request.form['value'])
     elif name == "windshield_wiper_status":
          gState.windshield_wiper_status = python_bool(request.form['value'])
     elif name == "door_status":
          gState.update_door(request.form['value'], python_bool(request.form['event']))
     else:
          print("Unsupported data received from UI: " + name)

     return _make_status_response(201)

def python_bool(value):
     if value == "true":
          return True
     if value == "false":
          return False
     else:
          return None

@app.route('/_get_data')
def get_data():
     return gState.dynamics_data

if __name__ == '__main__':
     global gState
     gState = state_manager.StateManager()

     flask_port = 50000

     print('For the UI, navigate a browser to localhost:' + str(flask_port))
     app.run(use_reloader=False, port=flask_port)
