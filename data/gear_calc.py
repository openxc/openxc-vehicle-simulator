from .data_calc import DataCalc

class GearCalc(DataCalc):
    def __init__(self, update_callback):
        self.initialize_data(update_callback)

    def initialize_data(self, update_callback):
        self.update = update_callback
        self.gear = 0
        self.gears = ['neutral', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth' ]
        self.data = self.gears[self.gear]
        self.speeds = [ [0, 0 ], [0, 25], [20, 50], [45, 75], [70, 100], [95, 125], [120, 500] ]

    def iterate(self, vehicle_speed, engine_running):  # Any necessary data should be passed in
        if vehicle_speed < self.speeds[self.gear][0]:
            self.gear = self.gear - 1
            self.data = self.gears[self.gear]
            self.update('transmission_gear_position', self.data)
        elif vehicle_speed > self.speeds[self.gear][1]:
            self.gear = self.gear + 1
            self.data = self.gears[self.gear]
            self.update('transmission_gear_position', self.data)
