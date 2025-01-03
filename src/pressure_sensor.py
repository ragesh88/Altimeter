import time

from sensor import Sensor, PRESSURE_SENSOR_TYPE

class PressureSensor(Sensor):
    def __init__(self, sensor_id: int, sensor_name: str, data_unit: int):
        super(PressureSensor, self).__init__(sensor_id, sensor_name, PRESSURE_SENSOR_TYPE,
                                             data_unit)

    def readCallback(self, data):
        """
        callback function for pressure sensor reading and pushes to data queue
        in the given unit
        """
        self.sensor_data_queue.put(data)
