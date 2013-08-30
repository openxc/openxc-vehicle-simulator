import threading
import time
import math
from flask import jsonify
import datetime

from data import speed_calc
from data import torque_calc
from data import engine_speed_calc
from data import fuel_consumed_calc
from data import odometer_calc

class DynamicsModel(object):
    def __init__(self):
        self._initialize_data()

        t = threading.Thread(target=self.physics_loop, name="Thread-Physics")
        t.setDaemon(True)
        t.start()

        print("Dynamics Model initialized")

    def _initialize_data(self):
        self.speed_data = speed_calc.SpeedCalc()
        self.torque_data = torque_calc.TorqueCalc()
        self.engine_speed_data = engine_speed_calc.EngineSpeedCalc()
        self.fuel_consumed_data = fuel_consumed_calc.FuelConsumedCalc()
        self.odometer_data = odometer_calc.OdometerCalc()

        self.delay_100Hz = datetime.timedelta(0,0,10000)
        self.next_iterate = datetime.datetime.now() + self.delay_100Hz
        self.zero_timedelta = datetime.timedelta(0,0,0)

        self.accelerator = 0.0
        self.brake = 0.0

    def physics_loop(self):
        while True:
            time_til_calc = self.next_iterate - datetime.datetime.now()
            if time_til_calc > self.zero_timedelta:
                time.sleep(time_til_calc.microseconds / 1000000.0)
                #Assuming less than a second.
            self.next_iterate = self.next_iterate + self.delay_100Hz
            
            self.speed_data.iterate(self.accelerator)
            self.torque_data.iterate(self.accelerator, self.vehicle_speed)
            self.engine_speed_data.iterate(self.vehicle_speed)
            self.fuel_consumed_data.iterate(self.accelerator)
            self.odometer_data.iterate(self.vehicle_speed)

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
        if self.brake > 0.0:
            return True
        else:
            return False

    @property
    def fuel_consumed(self):
        return self.fuel_consumed_data.get()

    @property
    def odometer(self):
        return self.odometer_data.get()

    @property
    def data(self):
        return jsonify(vehicle_speed=self.vehicle_speed,
                       torque_at_transmission=self.torque,
                       engine_speed=self.engine_speed,
                       fuel_consumed_since_restart=self.fuel_consumed,
                       odometer=self.odometer)
