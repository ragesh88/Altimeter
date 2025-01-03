"""
The script to simulate elevation estimation of the altimeter using logged pressure and gps sensor data.
Here elevation estimation with and without the gps sensor data is used for comparison. In the script,
the altimeter object is build by assembling the different components like sensors, sensor_models and filters
"""

from altimeter import Altimeter
from pressure_sensor import PressureSensor
from gps_sensor import GPSSensor
from sensor_model import PressureSensorModels, GPSSensorModels
from filters import MovingAverage1D
from data_logger import DataLogger
from simulation_utils import *

import toml
import matplotlib.pyplot as plt

def main():
    # loading the sensor data ground truth
    pressure_data_file = "../data/pressure_sensor_data.txt"
    gps_data_file = "../data/gps_sensor_data.txt"
    ground_truth_data_file = "../data/ground_truth_data.txt"
    time_stamps = []
    ground_truth_data = []
    with open(ground_truth_data_file, 'r') as f:
        for line in f.readlines():
            data = line.strip().split(',')
            time_stamps.append(float(data[0]))
            ground_truth_data.append(float(data[1]))

    # setting up the sensors with data
    pressure_sensor = PressureSensor(sensor_id=1, sensor_name="PressureSensor", data_unit='Pa')
    gps_sensor = GPSSensor(sensor_id=2, sensor_name="GpsSensor", data_unit='m')
    loadPressureData(pressure_sensor, pressure_data_file)
    loadGPSData(gps_sensor, gps_data_file)


    # setting up the sensor model
    pressure_sensor_model_name = 'standardAtmosModel'
    gps_sensor_model_name = 'standardGpsModel'
    pressure_sensor_model_config_file = '../cfg/standardAtmosModelParam.toml'
    gps_sensor_model_config_file = '../cfg/standardGpsModelParam.toml'
    pressure_sensor_model_parameters = toml.load(pressure_sensor_model_config_file)
    gps_sensor_model_parameters = toml.load(gps_sensor_model_config_file)
    pressure_sensor_model = PressureSensorModels(pressure_sensor_model_name, pressure_sensor_model_parameters)
    gps_sensor_model = GPSSensorModels(gps_sensor_model_name, gps_sensor_model_parameters)

    # setting up the filters to filter inherent noise from the sensor source
    pressure_sensor_filter_config_file = '../cfg/pressure_moving_avg_param.toml'
    gps_sensor_filter_config_file = '../cfg/gps_moving_avg_param.toml'
    pressure_filter_parameter = toml.load(pressure_sensor_filter_config_file)
    gps_sensor_filter_parameter = toml.load(gps_sensor_filter_config_file)
    pressure_sensor_filter = MovingAverage1D(pressure_filter_parameter)
    gps_sensor_filter = MovingAverage1D(gps_sensor_filter_parameter)
    pressure_data_buffer_size = 16


    # setting up the logger for logging data for future use
    log_file = '../logs/log.txt'
    data_logger = DataLogger(log_file)

    # setting up the altimeter
    altimeter = Altimeter(pressure_sensor, gps_sensor,
                 pressure_sensor_model, gps_sensor_model,
                 pressure_sensor_filter,
                 gps_sensor_filter, pressure_data_buffer_size,
                 data_logger)
    output_data = altimeter.run()

    # setting up the altimeter without gps for comparison
    loadPressureData(pressure_sensor, pressure_data_file)
    altimeter = Altimeter(pressure_sensor, gps_sensor,
                          pressure_sensor_model, gps_sensor_model,
                          pressure_sensor_filter,
                          gps_sensor_filter, pressure_data_buffer_size,
                          data_logger)
    output_data_without_gps = altimeter.run()

    # load the raw sensor measurements for plotting
    pressure_raw_data = []
    f = open(pressure_data_file, 'r')
    for data in f.readlines():
        d = data.split(',')
        pressure = float(d[1])
        pressure_raw_data.append(pressure)

    gps_raw_data = []
    gps_data_index = []
    f = open(gps_data_file, 'r')
    count = 0
    for data in f.readlines():
        d = data.split(',')
        if "None" not in d[1]:
            gps_data_index.append(count)
            gps_raw_data.append(float(d[3]))
        count += 1

    # generate the relevant plots
    plt.figure()
    plt.plot(pressure_raw_data, label='Pressure raw data in Pa')
    plt.xlabel("time steps")
    plt.legend()
    plt.savefig('../figures/pressure_data.png')
    plt.figure()
    plt.scatter(gps_data_index, gps_raw_data, label='GPS raw data m')
    plt.xlabel("time steps")
    plt.legend()
    plt.savefig('../figures/gps_raw_data.png')
    plt.xlabel("time steps")
    plt.figure()
    plt.plot(ground_truth_data, label='true elevation in m')
    plt.plot(output_data, label='estimated elevation in m')
    plt.plot(output_data_without_gps, label='estimated elevation without GPS')
    plt.legend()
    plt.savefig('../figures/estimation.png')
    plt.xlabel("time steps")
    plt.show()



if __name__ == "__main__":
    main()