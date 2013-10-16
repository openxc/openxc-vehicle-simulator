import threading
import time
import math
from flask import jsonify
import datetime

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
        self.speed_data = speed_calc.SpeedCalc()
        self.gear_data = gear_calc.GearCalc(update_callback)
        self.torque_data = torque_calc.TorqueCalc()
        self.engine_speed_data = engine_speed_calc.EngineSpeedCalc()
        self.fuel_consumed_data = fuel_consumed_calc.FuelConsumedCalc()
        self.odometer_data = odometer_calc.OdometerCalc()
        self.fuel_level_data = fuel_level_calc.FuelLevelCalc()
        self.heading_data = heading_calc.HeadingCalc()
        self.lat_data = lat_calc.LatCalc()
        self.lon_data = lon_calc.LonCalc()

        self.delay_100Hz = datetime.timedelta(0,0,10000)
        self.next_iterate = datetime.datetime.now() + self.delay_100Hz
        self.zero_timedelta = datetime.timedelta(0,0,0)

        self.accelerator = 0.0
        self.brake = 0.0
        self.steering_wheel_angle = 0.0
        self.parking_brake_status = False
        self.engine_running = True
        self.ignition_data = 'run'

        self.stopped = False

    def physics_loop(self):
        while True:
            if not self.stopped:
                time_til_calc = self.next_iterate - datetime.datetime.now()
                if time_til_calc > self.zero_timedelta:
                    time.sleep(time_til_calc.microseconds / 1000000.0)
                    #Assuming less than a second.
                self.next_iterate = self.next_iterate + self.delay_100Hz

                self.speed_data.iterate(self.accelerator, self.brake, self.parking_brake_status,
                                        self.engine_running)
                self.torque_data.iterate(self.accelerator, self.engine_speed, self.engine_running)
                self.gear_data.iterate(self.vehicle_speed, self.engine_running)
                self.engine_speed_data.iterate(self.vehicle_speed)
                self.fuel_consumed_data.iterate(self.accelerator, self.engine_running)
                self.odometer_data.iterate(self.vehicle_speed)
                self.fuel_level_data.iterate(self.fuel_consumed)
                self.heading_data.iterate(self.vehicle_speed, self.steering_wheel_angle)
                self.lat_data.iterate(self.vehicle_speed, self.heading_data.get())
                self.lon_data.iterate(self.vehicle_speed, self.heading_data.get(), self.lat)

# Properties  ---------------------
            
    @property
    def torque(self):
        return self.torque_data.get()

    @property
    def engine_speed(self):
        return self.engine_speed_data.get()

    @property
    def vehicle_speed(self):
        return math.fabs(self.speed_data.get())

    @property
    def brake_pedal_status(self):
        return self.brake > 0.0

    @property
    def fuel_consumed(self):
        return self.fuel_consumed_data.get()

    @property
    def odometer(self):
        return self.odometer_data.get()

    @property
    def fuel_level(self):
        return self.fuel_level_data.get()

    @property
    def lat(self):
        return self.lat_data.get()

    @property
    def lon(self):
        return self.lon_data.get()

    @property
    def data(self):
        return jsonify(vehicle_speed=self.vehicle_speed,
                       transmission_gear_posiotion=self.gear_data.get(),
                       torque_at_transmission=self.torque,
                       engine_speed=self.engine_speed,
                       fuel_consumed_since_restart=self.fuel_consumed,
                       odometer=self.odometer,
                       fuel_level=self.fuel_level,
                       latitude=self.lat,
                       longitude=self.lon)

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
