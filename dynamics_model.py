import threading
import time
import math
from flask import jsonify
import datetime
import json

from data import speed_calc
from data import gear_calc
from data import torque_calc
from data import engine_speed_calc
from data import fuel_consumed_calc
from data import odometer_calc
from data import fuel_level_calc
from data import heading_calc
from data import lat_calc
from data import lon_calc

class DynamicsModel(object):
    def __init__(self, update_callback):
        self._initialize_data(update_callback)

        t = threading.Thread(target=self.physics_loop, name="Thread-Physics")
        t.setDaemon(True)
        t.start()

        print("Dynamics Model initialized")

    def _initialize_data(self, update_callback):
        self.calculations = []
        self.calculations.append(speed_calc.SpeedCalc())
        self.calculations.append(gear_calc.GearCalc(update_callback))
        self.calculations.append(torque_calc.TorqueCalc())
        self.calculations.append(engine_speed_calc.EngineSpeedCalc())
        self.calculations.append(fuel_consumed_calc.FuelConsumedCalc())
        self.calculations.append(odometer_calc.OdometerCalc())
        self.calculations.append(fuel_level_calc.FuelLevelCalc())
        self.calculations.append(heading_calc.HeadingCalc())
        self.calculations.append(lat_calc.LatCalc())
        self.calculations.append(lon_calc.LonCalc())

        self.snapshot = {}
        for data in self.calculations:
            self.snapshot[data.name] = data.get()

        self.delay_100Hz = datetime.timedelta(0,0,10000)
        self.next_iterate = datetime.datetime.now() + self.delay_100Hz
        self.zero_timedelta = datetime.timedelta(0,0,0)

        self.accelerator = 0.0
        self.brake = 0.0
        self.steering_wheel_angle = 0.0
        self.parking_brake_status = False
        self.engine_running = True
        self.ignition_data = 'run'
        self.gear_lever = 'drive'

        self.snapshot['accelerator_pedal_position'] = self.accelerator
        self.snapshot['brake'] = self.brake
        self.snapshot['steering_wheel_angle'] = self.steering_wheel_angle
        self.snapshot['parking_brake_status'] = self.parking_brake_status
        self.snapshot['engine_running'] = self.engine_running
        self.snapshot['ignition_data'] = self.ignition_data

        self.stopped = False

    def physics_loop(self):
        while True:
            if not self.stopped:
                time_til_calc = self.next_iterate - datetime.datetime.now()
                if time_til_calc > self.zero_timedelta:
                    time.sleep(time_til_calc.microseconds / 1000000.0)
                    #Assuming less than a second.
                self.next_iterate = self.next_iterate + self.delay_100Hz

                new_snapshot = {}
                for data in self.calculations:
                    data.iterate(self.snapshot)
                    new_snapshot[data.name] = data.get()
                    
                # Store the latest user input...
                new_snapshot['accelerator_pedal_position'] = self.accelerator
                new_snapshot['brake'] = self.brake
                new_snapshot['steering_wheel_angle'] = self.steering_wheel_angle
                new_snapshot['parking_brake_status'] = self.parking_brake_status
                new_snapshot['engine_running'] = self.engine_running
                new_snapshot['ignition_data'] = self.ignition_data

                self.snapshot = new_snapshot
# Properties  ---------------------

    @property
    def torque(self):
        return self.snapshot['torque_at_transmission']

    @property
    def engine_speed(self):
        return self.snapshot['engine_speed']

    @property
    def vehicle_speed(self):
        return math.fabs(self.snapshot['vehicle_speed'])

    @property
    def brake_pedal_status(self):
        return self.brake > 0.0

    @property
    def fuel_consumed(self):
        return self.snapshot['fuel_consumed_since_restart']

    @property
    def odometer(self):
        return self.snapshot['odometer']

    @property
    def fuel_level(self):
        return self.snapshot['fuel_level']

    @property
    def lat(self):
        return self.snapshot['latitude']

    @property
    def lon(self):
        return self.snapshot['longitude']

    @property
    def data(self):
        return json.dumps(self.snapshot)

    @property
    def ignition_status(self):
        return self.ignition_data

    @ignition_status.setter
    def ignition_status(self, value):
        self.ignition_data = value
        if value == 'start':
            self.engine_running = True
        elif value == 'off':
            self.engine_running = False
        elif value == 'accessory':
            self.engine_running = False

    @property
    def gear_lever_position(self):
        return self.gear_lever

    @gear_lever_position.setter
    def gear_lever_position(self, value):
        self.gear_lever = value

    @property
    def transmission_gear_position(self):
        return self.snapshot['transmission_gear_position']
