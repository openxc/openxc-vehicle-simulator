from .data_calc import DataCalc

class EngineSpeedCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.data = 0.0
        self.name = 'engine_speed'

    def iterate(self, snapshot):
        vehicle_speed = snapshot['vehicle_speed']
        gear = snapshot['transmission_gear_int']
        
        self.data = 16382 * vehicle_speed / (100.0 * gear)
