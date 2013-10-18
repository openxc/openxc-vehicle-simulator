from .data_calc import DataCalc
from datetime import datetime
import math

class HeadingCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.data = 0.0
        self.last_calc = datetime.now()
        self.name = 'heading'

    def iterate(self, snapshot):
        vehicle_speed = snapshot['vehicle_speed']
        steering_wheel_angle = snapshot['steering_wheel_angle']
        
        # 600 degree steering == 45 degree wheels.
        wheel_angle = steering_wheel_angle / 13.33
        wheel_angle_rad = math.radians(wheel_angle)
        calc_angle = -wheel_angle_rad
        if wheel_angle < 0:
            calc_angle = calc_angle - (math.pi / 2)
        else:
            calc_angle = calc_angle + (math.pi / 2)
        # should return number between 28m and infinity
        turning_circumference_km = 0.028 * math.tan(calc_angle)

        current_time = datetime.now()
        time_delta = current_time - self.last_calc
        time_step = time_delta.seconds + (
                float(time_delta.microseconds) / 1000000)
        self.last_calc = current_time

        distance = time_step * (vehicle_speed / 3600 )  # Time * km/s.

        delta_heading = (distance / turning_circumference_km) * 2 * math.pi
        temp_heading = self.data + delta_heading
        while temp_heading >= (2*math.pi):
            temp_heading = temp_heading - (2*math.pi)
        while temp_heading < 0:
            temp_heading = temp_heading + (2*math.pi)

        self.data = temp_heading
