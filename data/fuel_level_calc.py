from .data_calc import DataCalc

class FuelLevelCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.data = 0.0
        self.tank_size = 40.0 #liters
        self.name = 'fuel_level'

    def iterate(self, snapshot):
        fuel_consumed = snapshot['fuel_consumed_since_restart']
        
        self.data = 100.0 * (self.tank_size - fuel_consumed) / self.tank_size
