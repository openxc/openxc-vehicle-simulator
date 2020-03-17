from .data_calc import DataCalc

class GearIntCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.data = 1
        self.speeds = [ [0, 0 ], [0, 25], [20, 50], [45, 75], [70, 100],
                [95, 125], [120, 500] ]
        self.name = 'transmission_gear_int'

    def shift_up(self):
        self.data = self.data + 1
        if self.data > 6:
            self.data = 6

    def shift_down(self):
        self.data = self.data - 1
        if self.data < 1:
            self.data = 1

    # Any necessary data should be passed in
    def iterate(self, snapshot):
        manual = snapshot['manual_trans']
        vehicle_speed = snapshot['vehicle_speed']
        engine_running = snapshot['engine_running']

        if not manual:
            if vehicle_speed < self.speeds[self.data][0]:
                self.data = self.data - 1
            elif vehicle_speed > self.speeds[self.data][1]:
                self.data = self.data + 1
