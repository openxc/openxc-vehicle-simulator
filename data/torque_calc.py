from .data_calc import DataCalc

class TorqueCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.data = 0.0
        self.engine_to_torque = 500.0 / 16382.0
        self.name = 'torque_at_transmission'
        self.gear_numbers = {'neutral':0, 'first':1, 'second':2, 'third':3,
                'fourth':4, 'fifth':5, 'sixth':6}

    # Any necessary data should be passed in
    def iterate(self, snapshot):
        accelerator = snapshot['accelerator_pedal_position']
        engine_speed = snapshot['engine_speed']
        engine_running = snapshot['engine_running']
        gear_number = self.gear_numbers[snapshot['transmission_gear_position']]
        gear_number = gear_number - 1  #First gear is the basline.
        if gear_number < 1:
            gear_number = 1

        # Giving sixth gear half the torque of first.
        gear_ratio = 1 - (gear_number * .1)
        
        drag = engine_speed * self.engine_to_torque
        power = accelerator * 15 * gear_ratio
        if engine_running:
            self.data = power - drag
        else:
            self.data = -drag
