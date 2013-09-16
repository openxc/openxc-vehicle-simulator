from .data_calc import DataCalc

class FuelLevelCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.data = 0.0
        self.tank_size = 40.0 #liters

    def iterate(self, fuel_consumed):  # Any necessary data should be passed in
        self.data = 100.0 * (self.tank_size - fuel_consumed) / self.tank_size

        return

