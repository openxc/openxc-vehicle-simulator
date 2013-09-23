from .data_calc import DataCalc

class EngineSpeedCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.data = 0.0

    def iterate(self, vehicle_speed):  # Any necessary data should be passed in
        self.data = 16382 * vehicle_speed / 200.0
        return

