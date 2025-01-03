import unittest
from pressure_sensor import PressureSensor
from gps_sensor import GPSSensor

class TestPressureSensor(unittest.TestCase):

    def setUp(self):
        self.sensor = PressureSensor(sensor_id=1, sensor_name="PressureSensor", data_unit='Pa')

    def testAddData(self):
        data = self.sensor.publish()
        self.assertEqual(data, None)
        test_data = [(1, 10), (2, None), (3, 30)]
        self.sensor.readCallback(test_data[0])
        self.sensor.readCallback(test_data[1])
        self.sensor.readCallback(test_data[2])
        self.assertEqual(self.sensor.sensor_data_queue.qsize(), len(test_data))
        data = self.sensor.publish()
        self.assertEqual(data[0], test_data[0][0])
        self.assertEqual(data[1], test_data[0][1])
        data = self.sensor.publish()
        self.assertEqual(data, None)
        data = self.sensor.publish()
        self.assertEqual(data[0], test_data[2][0])
        self.assertEqual(data[1], test_data[2][1])
        self.assertEqual(self.sensor.sensor_data_queue.qsize(), 0)
        data = self.sensor.publish()
        self.assertEqual(data, None)


class TestGPSSensor(unittest.TestCase):

    def setUp(self):
        self.sensor = PressureSensor(sensor_id=3, sensor_name="GPS sensor", data_unit='m')

    def testAddData(self):
        data = self.sensor.publish()
        self.assertEqual(data, None)
        test_data = [(1, 1, 2, 3), (2, 3, 5, 6), (3, None)]
        self.sensor.readCallback(test_data[0])
        self.sensor.readCallback(test_data[1])
        self.sensor.readCallback(test_data[2])
        self.assertEqual(self.sensor.sensor_data_queue.qsize(), len(test_data))
        data = self.sensor.publish()
        self.assertEqual(data[0], test_data[0][0])
        self.assertEqual(data[2], test_data[0][2])
        data = self.sensor.publish()
        self.assertEqual(data[0], test_data[1][0])
        self.assertEqual(data[2], test_data[1][2])
        data = self.sensor.publish()
        self.assertEqual(data, None)
        self.assertEqual(self.sensor.sensor_data_queue.qsize(), 0)
        data = self.sensor.publish()
        self.assertEqual(data, None)

if __name__ == '__main__':
    unittest.main()
