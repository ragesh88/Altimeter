import unittest
import numpy as np

from filters import *

class TestMovingAverage1D(unittest.TestCase):

    def setUp(self):
        filter_parameter = {'raw_data_window_size': 3, 'filtered_data_window_size': 0, 'weights': [2.0, 4.0, 2.0]}
        self.filter = MovingAverage1D(filter_parameter)

    def testMethodAttribute(self):
        with self.assertRaises(AssertionError):
            MovingAverage1D({})
        filter_parameter = {'raw_data_window_size': 3}
        with self.assertRaises(AssertionError):
            MovingAverage1D(filter_parameter)
        filter_parameter = {'filtered_data_window_size': 3}
        with self.assertRaises(AssertionError):
            MovingAverage1D(filter_parameter)
        filter_parameter = {'raw_data_window_size': 3, 'filtered_data_window_size': 0}
        with self.assertRaises(AssertionError):
            MovingAverage1D(filter_parameter)
        filter_parameter['weights'] = 0.5
        with self.assertRaises(AssertionError):
            MovingAverage1D(filter_parameter)
        filter_parameter['weights'] = [0.5, 0.5]
        with self.assertRaises(AssertionError):
            MovingAverage1D(filter_parameter)
        filter_parameter['weights'] = [1, 1, 1]

    def testMovingAvgAlgo(self):
        weights = [0.25, 0.5, 0.25]
        for w1, w2 in zip(weights, self.filter.weights):
            # test if weights are normalized
            self.assertEqual(w1, w2)
        test_data = [1.0, 3.0, 4.0, 2.0, 5.0, 6.0, 8.0, 9.0, 1.5]
        expected_filtered_data = []
        for i in range(len(test_data)-len(weights) + 1):
            expected_filtered_data.append(float(np.dot(np.array(weights), np.array(test_data[i:i+len(weights)]))))
        for i in range(len(test_data)-len(weights)+1, len(test_data)):
            expected_filtered_data.append(test_data[i])
        actual_filtered_data = []
        for i in range(len(test_data)-1,-1,-1):
            splitted_test_data = [test_data[j] for j in range(i, len(test_data))]
            splitted_test_data = splitted_test_data[::-1]
            actual_filtered_data.append(self.filter.apply(splitted_test_data, []))
        actual_filtered_data = actual_filtered_data[::-1]
        for actual, expected in zip(actual_filtered_data, expected_filtered_data):
            self.assertAlmostEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()