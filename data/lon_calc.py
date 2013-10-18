from .data_calc import DataCalc
from datetime import datetime
import math

class LonCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.data = -83.237275
        self.last_calc = datetime.now()
        self.earth_circumference_equator_km = 40075.0
        self.km_per_deg_equator = self.earth_circumference_equator_km / 360.0
        self.name = 'longitude'

    # Any necessary data should be passed in
    def iterate(self, snapshot):
        vehicle_speed = snapshot['vehicle_speed']
        heading = snapshot['heading']
        lat = snapshot['latitude']
        
        current_time = datetime.now()
        time_delta = current_time - self.last_calc
        self.last_calc = current_time
        time_step = time_delta.seconds + (
                float(time_delta.microseconds) / 1000000)

        distance = time_step * (vehicle_speed / 3600)
        E_W_dist = distance * math.sin(heading)

        lat_rad = math.radians(lat)

        km_per_deg = math.fabs(self.km_per_deg_equator * math.sin(lat_rad))

        delta_lon = E_W_dist / km_per_deg
        new_lon = self.data + delta_lon
        while new_lon >= 180.0:
            new_lon = new_lon - 360
        while new_lon < -180:
            new_lon = new_lon + 360

        self.data = new_lon
