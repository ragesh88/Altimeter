import unittest
from sensor_model import PressureSensorModels, GPSSensorModels

class TestPressureSensorModel(unittest.TestCase):

    def setUp(self):
        model_parameter = {'a': 3.0, 'b': 2.0, 'c': 1.0}
        self.sensor = PressureSensorModels("standardAtmosModel", model_parameter)

    def testMethodAttribute(self):
        with self.assertRaises(AssertionError):
            PressureSensorModels("random_model", {})

    def testStandardAtmosModel(self):
        with self.assertRaises(AssertionError):
            # ensure it handles only float data
            self.sensor.model(1)
        self.assertAlmostEqual(self.sensor.model(1.0), 1.0)
        self.sensor.sensor_model_parameters = {'a': 10.0, 'b': 2.0}
        with self.assertRaises(AssertionError):
            self.sensor.model(1.0)
        self.sensor.sensor_model_parameters['c'] = 0.5
        self.assertAlmostEqual(self.sensor.model(16.0), 2.0)



class TestGPSSensorModel(unittest.TestCase):

    def setUp(self):
        model_parameter = {}
        self.sensor = GPSSensorModels("standardGpsModel", model_parameter)

    def testMethodAttribute(self):
        with self.assertRaises(AssertionError):
            GPSSensorModels("random_model", {})

    def testStandardAtmosModel(self):
        with self.assertRaises(AssertionError):
            # ensure it handles only list of floats
            self.sensor.model(1)
        with self.assertRaises(AssertionError):
            # ensure it handles only list of floats with len 3
            self.sensor.model([1.0, 1.0])
        with self.assertRaises(AssertionError):
            # ensure it handles only list of floats with len 3
            self.sensor.model([1, 1.0, '1'])
        self.assertAlmostEqual(self.sensor.model([1.2, 2.3, 4.5]), 4.5)


if __name__ == '__main__':
    unittest.main()
