"""
The script to generate pressure and gps sensor data for testing
"""

import random

import numpy as np
import matplotlib.pyplot as plt

def main():
    pressure_file_name = "../data/pressure_sensor_data.txt"
    gps_file_name = "../data/gps_sensor_data.txt"
    ground_truth_file_name = "../data/ground_truth_data.txt"
    height_samples_pressure = 1000
    a, b, c = 44330.8, 4946.54, 0.1902632
    height_samples_gps = 1000
    x = np.linspace(1, 100, height_samples_pressure)
    # x = 10 + 190*np.sin(np.linspace(0, np.pi, height_samples_pressure))
    bias = np.linspace(0, 500, height_samples_pressure)
    pressure_data = np.power((a - x)/b, 1/c) +  np.random.normal(0, 100, size=len(x)) + bias
    estimate_height = a - b * np.power(pressure_data, c)
    plt.figure()
    plt.plot(x, x, label='true height')
    plt.plot(x, estimate_height, label='estimated height')
    plt.legend()
    plt.show()
    gps_data = x + np.random.normal(0, 1, size=len(x))
    plt.figure()
    plt.plot(x, x, label='true height')
    plt.plot(x, gps_data, label='estimated gps height')
    plt.legend()
    plt.show()
    with open(ground_truth_file_name, "w") as f:
        for i in range(len(x)):
            f.write(str(i) + ',' + str(x[i]) + '\n')

    with open(pressure_file_name, 'w') as f:
        for i in range(len(x)):
            f.write(str(i) + ',' + str(pressure_data[i]) + '\n')

    with open(gps_file_name, 'w') as f:
        for i in range(len(x)):
            if random.random() < 0.1:
                f.write(str(i) + ',' + str(gps_data[i]) + ',' + str(gps_data[i]) + ',' + str(gps_data[i]) + '\n')
            else:
                f.write(str(i) + ',' + "None" + '\n')


if __name__ == '__main__':
    main()