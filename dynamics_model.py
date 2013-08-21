import threading
import time
import math
from flask import jsonify

from data import speed_calc
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
        self.fuel_consumed_data = fuel_consumed_calc.FuelConsumedCalc()
        self.odometer_data = odometer_calc.OdometerCalc()
        self.accelerator = 0.0

    def physics_loop(self):
        while True:
            self.speed_data.iterate(self.accelerator)
            time.sleep(0.0034)
            self.fuel_consumed_data.iterate(self.accelerator)
            time.sleep(0.0034)
            self.odometer_data.iterate(self.vehicle_speed)
            time.sleep(0.0034)

    @property
    def vehicle_speed(self):
        return math.fabs(self.speed_data.get())

    @property
    def fuel_consumed(self):
        return self.fuel_consumed_data.get()

    @property
    def odometer(self):
        return self.odometer_data.get()

    @property
    def data(self):
        return jsonify(vehicle_speed=self.vehicle_speed,
                    fuel_consumed_since_restart=self.fuel_consumed,
                    odometer=self.odometer)
