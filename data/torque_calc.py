from .data_calc import DataCalc

class TorqueCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.data = 0.0

    def iterate(self, accelerator, vehicle_speed):  # Any necessary data should be passed in
        torque = self.data + 1
        if torque > 1500:
            torque = -500
        self.data = torque
        return

