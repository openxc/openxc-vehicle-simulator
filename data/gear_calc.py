from .data_calc import DataCalc

class GearCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.gears = ['neutral', 'first', 'second', 'third', 'fourth',
                'fifth', 'sixth' ]
        self.data = self.gears[0]
        self.name = 'transmission_gear_position'

    # Any necessary data should be passed in
    def iterate(self, snapshot):
        gear = snapshot['transmission_gear_int']
        self.data = self.gears[gear]
