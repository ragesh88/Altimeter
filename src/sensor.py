import time
from abc import ABC, abstractmethod
from time import time_ns
from queue import Queue

PRESSURE_SENSOR_TYPE = 0
GPS_SENSOR_TYPE = 1

class Sensor(ABC):
    """
    The generic sensor abstract base class. The class defines the interface for sensor
    """
    def __init__(self, sensor_id: int, sensor_name: str, sensor_type:int,
                 data_unit: int):
        self.sensor_id = sensor_id
        self.sensor_name = sensor_name
        self.sensor_type = sensor_type
        self.sensor_data_unit = data_unit
        self.sensor_data_queue = Queue()

    @abstractmethod
    def readCallback(self, data):
        """
        callback function for sensor reading and pushes to data queue
        should be implemented in subclass
        """
        pass

    def publish(self):
        """
        reads the data from the data queue and publishes it
        :return: tuple time, sensor_data
        """
        if self.sensor_data_queue.empty():
            return None
        data = self.sensor_data_queue.get()
        if data[1] is None:
            return None
        return data
