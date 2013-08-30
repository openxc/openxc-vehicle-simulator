from .data_calc import DataCalc
from datetime import datetime

class HeadingCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.data = 0.0
        self.last_calc = datetime.now()

    def iterate(self, vehicle_speed, steering_wheel_angle):  # Any necessary data should be passed in
        current_time = datetime.now()
        time_delta = current_time - self.last_calc
        time_step = time_delta.seconds + (float(time_delta.microseconds) / 1000000)
        self.last_calc = current_time

        return

