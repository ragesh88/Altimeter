"""
package with utility functions to aid simulation
"""
from pressure_sensor import PressureSensor
from gps_sensor import GPSSensor

def loadPressureData(pressure_sensor: PressureSensor, filename: str):
    """
    The function loads the pressure data from the given file to internal queue of the sensor object
    """
    f = open(filename, 'r')
    for data in f.readlines():
        d = data.split(',')
        time = float(d[0])
        pressure = float(d[1])
        pressure_sensor.readCallback((time, pressure))

def loadGPSData(gps_sensor: GPSSensor, filename: str):
    """
    The function loads the gps data from the given file to internal queue of the sensor object
    """
    f = open(filename, 'r')
    for data in f.readlines():
        d = data.split(',')
        time = float(d[0])
        if "None" in d[1]:
            gps_sensor.readCallback((time, None))
        else:
            gps_sensor.readCallback((time, float(d[1]), float(d[2]), float(d[3])))

def pressureGpsLogDataSplitter(log_filename: str, pressure_data_filename: str, gps_data_filename: str):
    """
    This function will split logged data in the log file to pressure and gps data files. This is done so that
    the files can be read in parallel to simulate the sensor readings.
    :param log_filename: input log file path
    :param pressure_data_filename: output pressure data file path
    :param gps_data_filename: output gps data file path
    """
    f = open(log_filename, 'r')
    prev_sensor, prev_time = None, None
    save_data = {'pressure_sensor': [], 'gps_sensor': []}
    for data in f.readlines():
        d = data.split()
        time = (d[0].strip('[').strip(']'))
        sensor = d[1]
        value = ""
        for i in range(2, len(d)):
            value += d[i].strip('(').strip(')')

        save_data[sensor].append((time + ',' + value))
        if prev_sensor and prev_time and sensor == prev_sensor and float(time) == float(prev_time)+1:
            if 'pressure' in sensor:
                save_data['gps_sensor'].append((time + ',' +  "None"))
            else:
                save_data['pressure_sensor'].append((time + ',' +  "None"))
        prev_sensor, prev_time = sensor, time

    # write the data set to respective files
    with open(pressure_data_filename, 'w') as f:
        for data in save_data['pressure_sensor']:
            f.write(str(data) + '\n')
    with open(gps_data_filename, 'w') as f:
        for data in save_data['gps_sensor']:
            f.write(str(data) + '\n')


if __name__ == '__main__':
    log_filename = '../logs/log.txt'
    pressure_data_filename = '../data/test_pressure.txt'
    gps_data_filename = '../data/test_gps.txt'

    pressureGpsLogDataSplitter(log_filename, pressure_data_filename, gps_data_filename)
