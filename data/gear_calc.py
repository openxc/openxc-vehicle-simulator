from .data_calc import DataCalc

class GearCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.gear = 0
        self.gears = ['neutral', 'first', 'second', 'third', 'fourth',
                'fifth', 'sixth' ]
        self.data = self.gears[self.gear]
        self.speeds = [ [0, 0 ], [0, 25], [20, 50], [45, 75], [70, 100],
                [95, 125], [120, 500] ]
        self.name = 'transmission_gear_position'

    # Any necessary data should be passed in
    def iterate(self, snapshot):
        vehicle_speed = snapshot['vehicle_speed']
        engine_running = snapshot['engine_running']
        
        if vehicle_speed < self.speeds[self.gear][0]:
            self.gear = self.gear - 1
            self.data = self.gears[self.gear]
        elif vehicle_speed > self.speeds[self.gear][1]:
            self.gear = self.gear + 1
            self.data = self.gears[self.gear]
