import threading
import time

from data import speed_calc

class DynamicsModel():
    def __init__(self):
        self._initialize_data()

        t = threading.Thread(target=self.physics_loop, name="Thread-Physics")
        t.setDaemon(True)
        t.start()

        print("Dynamics Model initialized")

    def _initialize_data(self):
        self.speed_data = speed_calc.SpeedCalc()
        self.accelerator = 0.0

    def physics_loop(self):
        while True:
            self.speed_data.iterate(self.accelerator)
            time.sleep(0.01)

    @property
    def vehicle_speed(self):
        return self.speed_data.get()
