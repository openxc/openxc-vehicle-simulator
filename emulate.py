#!/usr/bin/env python

# all the imports

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
        render_template, flash, jsonify
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
     
     try:
          angle = float(request.form['angle'])
          if angle is not None:
               gState.steering_wheel_angle = angle
     except:
          pass

     try:
          accelerator = float(request.form['accelerator'])
          if accelerator is not None:
               gState.accelerator_pedal_position = accelerator
     except:
          pass

     try:
          brake = float(request.form['brake'])
          if brake is not None:
               gState.brake_pedal_position = brake
     except:
          pass

     try:
          parking_brake_status = python_bool(request.form['parking_brake_status'])
          if parking_brake_status is not None:
               gState.parking_brake_status = parking_brake_status
     except:
          pass

     try:
          ignition_status = python_bool(request.form['ignition_status'])
          if ignition_status is not None:
               gState.ignition_status = ignition_status
     except:
          pass

     try:
          headlamp_status = python_bool(request.form['headlamp_status'])
          if headlamp_status is not None:
               gState.headlamp_status = headlamp_status
     except:
          pass

     try:
          high_beam_status = python_bool(request.form['high_beam_status'])
          if high_beam_status is not None:
               gState.high_beam_status = high_beam_status
     except:
          pass

     try:
          windshield_wiper_status = python_bool(request.form['windshield_wiper_status'])
          if windshield_wiper_status is not None:
               gState.windshield_wiper_status = windshield_wiper_status
     except:
          pass

     return redirect(url_for('vehicle_data'))

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

     app.run(use_reloader=False, host='0.0.0.0')
