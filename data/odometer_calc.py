from .data_calc import DataCalc
from datetime import datetime

class OdometerCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.data = 0.0
        self.last_calc = datetime.now()
        self.KPH_to_KPS = 60 * 60
        self.name = 'odometer'

    def iterate(self, snapshot):
        vehicle_speed = snapshot['vehicle_speed']  # Any necessary data should be passed in

        current_time = datetime.now()
        time_delta = current_time - self.last_calc
        time_step = time_delta.seconds + (
                float(time_delta.microseconds) / 1000000)
        self.last_calc = current_time

        self.data = self.data + (vehicle_speed * time_step / self.KPH_to_KPS)
