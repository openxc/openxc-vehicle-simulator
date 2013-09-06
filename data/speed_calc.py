from .data_calc import DataCalc
import math
from datetime import datetime

class SpeedCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.data = 0.0
        self.last_calc = datetime.now()

    def iterate(self, accelerator_percent):  # Any necessary data should be passed in
        AIR_DRAG_COEFFICIENT = .000008
        ENGINE_DRAG_COEFFICIENT = 0.02
        ENGINE_V0_FORCE = 20 #units are cars*km/h/s
        CAR_MASS = 1  # Specifically, one car.
        speed = self.data  #Just to avoid confution

        air_drag = speed * speed * speed * AIR_DRAG_COEFFICIENT
        
        engine_drag = speed * ENGINE_DRAG_COEFFICIENT

        engine_force = (ENGINE_V0_FORCE * accelerator_percent / 100)  # accelerator_percent is 0.0 to 100.0, not 0

        if speed > 0.1:
            road_friction = .1
        else:
            road_friction = speed
        
        acceleration = engine_force - air_drag - engine_drag - road_friction
        
        current_time = datetime.now()

        time_delta = current_time - self.last_calc
        time_step = time_delta.seconds + (float(time_delta.microseconds) / 1000000)
        self.last_calc = current_time

        self.data = speed + ( acceleration * time_step)
