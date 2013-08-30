from .data_calc import DataCalc
from datetime import datetime

class LonCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.data = -83.237275
        self.last_calc = datetime.now()

    def iterate(self, vehicle_speed, heading, lat):  # Any necessary data should be passed in
        current_time = datetime.now()
        time_delta = current_time - self.last_calc
        time_step = time_delta.seconds + (float(time_delta.microseconds) / 1000000)
        self.last_calc = current_time

        return

