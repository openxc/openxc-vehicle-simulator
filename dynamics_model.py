import threading
import time
import math

from data import speed_calc
from data import fuel_consumed_calc

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
        self.accelerator = 0.0

    def physics_loop(self):
        while True:
            self.speed_data.iterate(self.accelerator)
            time.sleep(0.005)
            self.fuel_consumed_data.iterate(self.accelerator)
            time.sleep(0.005)

    @property
    def vehicle_speed(self):
        return math.fabs(self.speed_data.get())

    @property
    def fuel_consumed(self):
        return math.fabs(self.fuel_consumed_data.get())
