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
     flash('Updates halted.')
     session['updates_paused'] = True
     global gState
     gState.pause()
     return redirect(url_for('vehicle_data'))

@app.route('/single', methods=['POST'])
def single():
     #make a global socket
     flash('Single packet sent.')
     global gState
     gState.update_once()
     return redirect(url_for('vehicle_data'))

@app.route('/start', methods=['POST'])
def start():
     #make a global socket
     flash('Updates resumed.')
     session.pop('updates_paused', None)
     global gState
     gState.resume()
     return redirect(url_for('vehicle_data'))

@app.route('/steering', methods=['POST'])
def update_steering_wheel():
     angle = float(request.form['angle'])
     msg = 'Steering Wheel Angle set to %d' % angle
     print(msg)
     flash(msg)
     global gState
     gState.steering_wheel_angle = angle
     return redirect(url_for('vehicle_data'))

@app.route('/accelerator', methods=['POST'])
def update_accelerator():
     accelerator = float(request.form['accelerator'])
     if (accelerator >= 0) and (accelerator <= 100):
          msg = "Accelerator Percentage set to %d" % accelerator
          print(msg)
          flash(msg)
          global gState
          gState.accelerator_pedal_position = accelerator
     else:
          flash('Accelerator Percentage must be between 0 and 100.')
     return redirect(url_for('vehicle_data'))

@app.route('/_get_data')
def get_data():
     return jsonify(vehicle_speed=gState.vehicle_speed,
                    fuel_consumed_since_restart=gState.fuel_consumed )

if __name__ == '__main__':
     print('Running Main...')
     global gState
     gState = state_manager.StateManager()

     app.run(use_reloader=False)
