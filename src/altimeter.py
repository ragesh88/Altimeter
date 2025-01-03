import time
import numpy as np
from typing import Any

from pressure_sensor import PressureSensor
from gps_sensor import GPSSensor
from sensor_model import PressureSensorModels, GPSSensorModels
from filters import Filters
from data_logger import DataLogger


class Altimeter:
    """
    The class to build an altimeter using pressure sensor and GPS sensor. This class assumes that
    the pressure sensor data is periodic and the Gps sensor data is sporadic. Therefore, this altimeter
    relies on primarily on pressure sensor data to estimate the elevation and uses the gps data to estimate
    the bias in the pressure sensor data and corrects it.
    """
    def __init__(self, pressure_sensor: PressureSensor, gps_sensor: GPSSensor,
                 pressure_sensor_model: PressureSensorModels, gps_sensor_model: GPSSensorModels,
                 pressure_sensor_filter: Filters, gps_sensor_filter: Filters,
                 pressure_data_buffer_size: int, data_logger: DataLogger,
                 gps_data_size_factor = 0.5,
                 max_idle_time=5.0):
        """

        :param pressure_sensor: Object to query pressure sensor data.
        :param gps_sensor: Object to query GPS sensor data.
        :param pressure_sensor_model: sensor model to convert the pressure sensor data to elevation.
        :param gps_sensor_model: sensor model to convert the GPS sensor data to elevation.
        :param pressure_sensor_filter: filter to filter inherent source noisy in the pressure sensor data.
        :param gps_sensor_filter: filter to filter inherent source noisy in the GPS sensor data.
        :param pressure_data_buffer_size: maximum of the internal buffer to hold past pressure sensor data.
        :param data_logger: DataLogger object to log data for future simulation
        :param gps_data_size_factor: ratio of gps data buffer size to pressure data buffer size.
        :param max_idle_time: maximum idle time in seconds while waiting for sensor inputs
        """
        self.pressure_sensor = pressure_sensor
        self.gps_sensor = gps_sensor
        self.pressure_sensor_model = pressure_sensor_model
        self.gps_sensor_model = gps_sensor_model
        self.pressure_sensor_filter = pressure_sensor_filter
        self.gps_sensor_filter = gps_sensor_filter
        self.pressure_data_buffer_size = pressure_data_buffer_size
        self.data_logger = data_logger
        self.gps_data_size_factor = gps_data_size_factor
        self.max_idle_time = max_idle_time  # in seconds
        self.state = 0.0
        self.output_data = []

    def readData(self):
        """
        Reads the pressure sensor and GPS sensor using the respective sensor object and
        logs the data for future simulation.
        If no data is received from either of the sensors within the maximum idle time, then
        break_status to false and returned to end the data processing
        :return: pressure data, gps data, break_status
        """
        break_status = False
        pressure_data, gps_data = self.pressure_sensor.publish(), self.gps_sensor.publish()
        if pressure_data or gps_data:
            self.last_activity_time = time.time()
            if pressure_data:
                self.data_logger.log(pressure_data[0], 'pressure_sensor', pressure_data[1])
            if gps_data:
                self.data_logger.log(gps_data[0], 'gps_sensor', (gps_data[1], gps_data[2], gps_data[3]))
        else:
            # break the loop if both data is absent for a long time
            if time.time() - self.last_activity_time > self.max_idle_time:
                break_status = True
        return pressure_data, gps_data, break_status

    def filterAndUpdateDataBuffer(self, raw_sensor_data:dict[Any], filtered_sensor_data: dict[Any], data: Any,
                                  sensor_name: str, buffer_size_limit: int):
        """
        takes the raw sensor data and filters it and updates the internal buffer. The internal buffer is also monitored
        to avoid buffer overflow.
        :param raw_sensor_data: internal buffer for raw sensor data
        :param filtered_sensor_data: internal buffer for filtered sensor data
        :param data: sensor data as float or List[float]
        :param sensor_name: name of the sensor
        :param buffer_size_limit: maximum buffer size
        """
        if len(filtered_sensor_data[sensor_name]['data']) == buffer_size_limit:
            filtered_sensor_data[sensor_name]['data'].pop(0)
            filtered_sensor_data[sensor_name]['time'].pop(0)
            raw_sensor_data[sensor_name]['time'].pop(0)
            raw_sensor_data[sensor_name]['data'].pop(0)
        raw_sensor_data[sensor_name]['time'].append(data[0])
        raw_sensor_data[sensor_name]['data'].append(data[1])
        filtered_pressure_data = self.pressure_sensor_filter.apply(raw_sensor_data[sensor_name]['data'],
                                                                   filtered_sensor_data[sensor_name]['data'])
        filtered_sensor_data[sensor_name]['time'].append(data[0])
        filtered_sensor_data[sensor_name]['data'].append(filtered_pressure_data)


    def processSensorData(self):
        """
        The primarily routine responsible for estimating the elevation using pressure sensor and gps sensor data.
        The function reads the sensor data, compute the mean of the filtered sensor data in the internal buffers,
        computes the bias as the difference between the mean of pressure and gps buffer data. The bias is used to
        correct the dift error in elevation estimate based on the pressure sensor data. The output is store in the list
        output_data
        :return:
        """
        self.last_activity_time = time.time()
        filtered_sensor_data, raw_sensor_data = ({'pressure_sensor': {'data': [], 'time':[]},
                                                    'gps_sensor': {'data': [], 'time':[]}},
                                                   {'pressure_sensor': {'data': [], 'time':[]},
                                                    'gps_sensor': {'data': [], 'time':[]}})
        bias = 0.0
        sample_mean_filtered_pressure_elevations = 0.0
        estimated_elevation = 0.0
        self.data_logger.start()
        while True:
            # read data from sensors
            pressure_data, gps_data, break_status = self.readData()
            if break_status:
                # break if data is not available for a long time
                break
            if pressure_data:
                # processing pressure data
                self.filterAndUpdateDataBuffer(raw_sensor_data, filtered_sensor_data, pressure_data, sensor_name='pressure_sensor',
                                               buffer_size_limit=self.pressure_data_buffer_size)
                estimated_elevations = [self.pressure_sensor_model.model(data) for data in filtered_sensor_data['pressure_sensor']['data']]
                sample_mean_filtered_pressure_elevations = sum(estimated_elevations) / len(estimated_elevations)
                estimated_elevation = estimated_elevations[-1]

            if gps_data:
                # processing gps data
                elevation_gps = self.gps_sensor_model.model([gps_data[1], gps_data[2], gps_data[3]])
                self.filterAndUpdateDataBuffer(raw_sensor_data, filtered_sensor_data, [gps_data[0], elevation_gps],
                                               sensor_name='gps_sensor',
                                               buffer_size_limit=int(self.gps_data_size_factor * self.pressure_data_buffer_size))
                sample_mean_filtered_gps = (sum(filtered_sensor_data['gps_sensor']['data']) /
                                            len(filtered_sensor_data['gps_sensor']['data']))
                # compute bias for the estimate
                bias = sample_mean_filtered_gps - sample_mean_filtered_pressure_elevations
            if pressure_data or gps_data:
                corrected_elevation = estimated_elevation + bias
                self.state = corrected_elevation
                self.output_data.append(corrected_elevation)

    def run(self):
        """
        The routine responsible for running the elevation estimation algorithm.
        :return: output data as list[float]
        """
        self.data_logger.start()
        self.processSensorData()
        self.data_logger.stop()
        return self.output_data
