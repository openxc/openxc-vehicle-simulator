from .data_calc import DataCalc
import math
from datetime import datetime

class SpeedCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.speed = 0.0
        self.last_calc = datetime.now()

    def get(self):
        return math.fabs(self.speed)

    def put(self, new_value):
        self.speed = new_value

    def old_iterate(self, accelerator_percent):
        target_speed = accelerator_percent * 1.5

        speed_difference = target_speed - self.speed

        speed_difference = speed_difference * 0.001

        self.speed = self.speed + speed_difference

    def iterate(self, accelerator_percent):  # Any necessary data should be passed in
        AIR_DRAG_COEFFICIENT = .000006
        ENGINE_DRAG_COEFFICIENT = 0
        ROAD_FRICTION = .01
        ENGINE_V0_FORCE = 20 #units are cars*km/s^2
        CAR_MASS = 1  # Specifically, one car.

        air_drag = self.speed * self.speed * self.speed * AIR_DRAG_COEFFICIENT

        engine_drag = self.speed * ENGINE_DRAG_COEFFICIENT

        engine_force = (ENGINE_V0_FORCE * accelerator_percent / 100)  # accelerator_percent is 0.0 to 100.0, not 0
        
        acceleration = engine_force - air_drag - engine_drag - ROAD_FRICTION

        current_time = datetime.now()

        time_delta = current_time - self.last_calc
        time_step = time_delta.seconds + (float(time_delta.microseconds) / 1000000)
        self.last_calc = current_time

        self.speed = self.speed + ( acceleration * time_step)
