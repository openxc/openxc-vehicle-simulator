import threading
import time
from data import SpeedCalc

class DynamicsModel():
    def __init__(self):
        self.initializeData()

        t = threading.Thread(target=self.physics_loop, name="Thread-Physics")
        t.setDaemon(True)
        t.start()
        
        print "Dynamics Model initialized"

    def initializeData(self):
        self.speed_data = SpeedCalc.SpeedCalc()
        self.accelerator = 0.0

    def physics_loop(self):
        while True:
            self.speed_data.iterate(self.accelerator)
            time.sleep(0.01)

    def set_accel(self, new_value):
        self.accelerator = new_value

    def get_vehicle_speed(self):
        return self.speed_data.get()
