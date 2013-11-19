from .data_calc import DataCalc
from datetime import datetime

class FuelConsumedCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.data = 0.0
        self.last_calc = datetime.now()
        self.max_fuel = 0.0015 #In liters per second at full throttle.
        self.idle_fuel = 0.000015
        self.name = 'fuel_consumed_since_restart'

    # Any necessary data should be passed in
    def iterate(self, snapshot):
        accelerator_percent = snapshot['accelerator_pedal_position']
        ignition_status = snapshot['engine_running']
        
        current_time = datetime.now()
        time_delta = current_time - self.last_calc
        time_step = time_delta.seconds + (
                float(time_delta.microseconds) / 1000000)
        self.last_calc = current_time

        if ignition_status:
            self.data = self.data + self.idle_fuel + (self.max_fuel * (
                accelerator_percent / 100) * time_step)
