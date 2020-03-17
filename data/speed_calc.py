from .data_calc import DataCalc
import math
from datetime import datetime

class SpeedCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.data = 0.0
        self.last_calc = datetime.now()
        self.name = 'vehicle_speed'

    def iterate(self, snapshot):
        accelerator_percent = snapshot['accelerator_pedal_position']
        brake = snapshot['brake']
        parking_brake_status = snapshot['parking_brake_status']
        ignition_status = snapshot['engine_running']
        engine_speed = snapshot['engine_speed']
        gear = snapshot['transmission_gear_int']

        # Any necessary data should be passed in
        AIR_DRAG_COEFFICIENT = .000008
        ENGINE_DRAG_COEFFICIENT = 0.0004
        BRAKE_CONSTANT = 0.1
        ENGINE_V0_FORCE = 20 #units are cars*km/h/s
        CAR_MASS = 1  # Specifically, one car.
        speed = self.data  #Just to avoid confution

        air_drag = speed * speed * speed * AIR_DRAG_COEFFICIENT

        engine_drag = engine_speed * ENGINE_DRAG_COEFFICIENT

        if ignition_status:
            # accelerator_percent is 0.0 to 100.0, not 0
            engine_force = (ENGINE_V0_FORCE * accelerator_percent / (50 * gear))
        else:
            engine_force = 0.0

        acceleration = engine_force - air_drag - engine_drag - .1 - (
                brake * BRAKE_CONSTANT)

        if parking_brake_status:
            acceleration = acceleration - (BRAKE_CONSTANT * 100)

        current_time = datetime.now()

        time_delta = current_time - self.last_calc
        time_step = time_delta.seconds + (
                float(time_delta.microseconds) / 1000000)
        self.last_calc = current_time

        impulse = acceleration * time_step
        if (impulse + speed ) < 0.0:    #Will result in backward motion
            impulse = -speed

        self.data = speed + impulse
