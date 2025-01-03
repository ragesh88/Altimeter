import time
from random import random

from sensor import Sensor, GPS_SENSOR_TYPE

class GPSSensor(Sensor):
    def __init__(self, sensor_id: int, sensor_name: str, data_unit: int):
        super(GPSSensor, self).__init__(sensor_id, sensor_name, GPS_SENSOR_TYPE, data_unit)

    def readCallback(self, data):
        """
        callback function for pressure sensor reading and pushes to data queue
        in the given unit
        """
        self.sensor_data_queue.put(data)