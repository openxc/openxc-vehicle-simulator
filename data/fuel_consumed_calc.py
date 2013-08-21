from datetime import datetime

class FuelConsumedCalc(object):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.fuel_consumed = 0.0
        self.last_calc = datetime.now()
        self.max_fuel = 0.0015 #In liters per second at full throttle.
        self.idle_fuel = 0.000015

    def get(self):
        return self.fuel_consumed

    def iterate(self, accelerator_percent):  # Any necessary data should be passed in
        current_time = datetime.now()
        time_delta = current_time - self.last_calc
        time_step = time_delta.seconds + (float(time_delta.microseconds) / 1000000)
        self.last_calc = current_time

        self.fuel_consumed = self.fuel_consumed + self.idle_fuel + (self.max_fuel * (accelerator_percent / 100) * time_step)
        
        return

