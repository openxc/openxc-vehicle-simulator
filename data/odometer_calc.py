from datetime import datetime

class OdometerCalc(object):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.odometer = 0.0
        self.last_calc = datetime.now()
        self.KPH_to_KPS = 60 * 60

    def get(self):
        return self.odometer

    def iterate(self, vehicle_speed):  # Any necessary data should be passed in
        current_time = datetime.now()
        time_delta = current_time - self.last_calc
        time_step = time_delta.seconds + (float(time_delta.microseconds) / 1000000)
        self.last_calc = current_time

        self.odometer = self.odometer + (vehicle_speed * time_step / self.KPH_to_KPS)

        return

