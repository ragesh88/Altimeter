from sensor import PRESSURE_SENSOR_TYPE, GPS_SENSOR_TYPE
from typing import List

class SensorModel:
    """
    This class is the base class for all sensor models. A sensor model that sensing data
    and computes a parameter of interest. Eg a standard atmospheric pressure model can be
    used to compute elevation based on a pressure sensor information
    """
    def __init__(self, sensor_type: int, model):
        self.sensor_type = sensor_type
        self.model = model

class PressureSensorModels(SensorModel):
    def __init__(self, sensor_model: str, sensor_model_parameters: dict[str, float]):
        assert hasattr(self, sensor_model), f"invalid sensor model: {sensor_model}"
        super().__init__(PRESSURE_SENSOR_TYPE,  getattr(self, sensor_model))
        self.sensor_model_parameters = sensor_model_parameters

    def standardAtmosModel(self, pressure_data):
        """
        standard atmospheric pressure sensor model to convert pressure sensor
        model to elevation measurements based on: "Portland State Aerospace Society, “A Quick Derivation
        relating altitude to air pressure,” Tech. Rep., Portland State Aerospace Society, 2004"
        :param pressure_data: pressure data in Pa
        :return: height in meters
        """
        assert "a" in self.sensor_model_parameters, "model parameter a missing"
        assert "b" in self.sensor_model_parameters, "model parameter b missing"
        assert "c" in self.sensor_model_parameters, "model parameter c missing"
        assert type(pressure_data) == float, "pressure data must be a float"
        a = self.sensor_model_parameters['a']
        b = self.sensor_model_parameters['b']
        c = self.sensor_model_parameters['c']
        return a - b * (pressure_data ** c)

class GPSSensorModels(SensorModel):
    def __init__(self, sensor_model: str, sensor_model_parameters: dict[str, float]):
        assert hasattr(self, sensor_model), f"invalid sensor model: {sensor_model}"
        super().__init__(GPS_SENSOR_TYPE, getattr(self, sensor_model))
        self.sensor_model_parameters = sensor_model_parameters

    def standardGpsModel(self, gps_data: List[float]):
        """
        :param gps_data: a list with three float elements with latitude, longitude & elevation
        coordinates in order
        :return: the elevation in meters
        """
        assert type(gps_data) == list, "gps_data must be a list"
        assert len(gps_data) == 3, "invalid gps data"
        assert type(gps_data[0]) == float and type(gps_data[1])== float and type(gps_data[2])== float, "invalid gps data"
        return gps_data[2]