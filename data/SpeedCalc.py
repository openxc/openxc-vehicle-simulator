from DataCalc import DataCalc
import math

class SpeedCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.speed = 0.0

    def get(self):
        return math.fabs(self.speed)

    def put(self, new_value):
        self.speed = new_value

    def iterate(self, accelerator_percent):
        target_speed = accelerator_percent * 1.5

        speed_difference = target_speed - self.speed

        speed_difference = speed_difference * 0.001

        self.speed = self.speed + speed_difference
        
    def proper_iterate(self, accelerator_percent):  # Any necessary data should be passed in
        AIR_DRAG_COEFFICIENT = .1
        ENGINE_DRAG_COEFFICIENT = .1
        ROAD_FRICTION = .1
        ENGINE_V0_FORCE = 100000
        CAR_MASS = 500
        TIME_STEP = .01
        
        air_drag = self.speed * self.speed * AIR_DRAG_COEFFICIENT

        engine_drag = self.speed * ENGINE_DRAG_COEFFICIENT

        engine_force = (ENGINE_V0_FORCE * accelerator_percent / 100)  # accelerator_percent is 0.0 to 100.0, not 0
        if self.speed > 1.0:
            engine_force = engine_force / self.speed

        force = engine_force - air_drag - engine_drag - ROAD_FRICTION

        acceleration = force / CAR_MASS

        self.speed = self.speed + ( acceleration * TIME_STEP)
