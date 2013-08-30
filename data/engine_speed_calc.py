from .data_calc import DataCalc

class EngineSpeedCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.data = 0.0

    def iterate(self, vehicle_speed):  # Any necessary data should be passed in
        engine_speed = self.data + 1
        if engine_speed > 16382:
            engine_speed = 0
        self.data = engine_speed
        return

