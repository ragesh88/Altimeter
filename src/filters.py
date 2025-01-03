from abc import abstractmethod
from typing import Any

class Filters:
    """
    A generic filters class. Any new filters should inherit from this class.
    """
    def __init__(self, filter_parameters: dict[str, Any]):
        self.filter_parameters = filter_parameters
        assert "raw_data_window_size" in self.filter_parameters
        assert "filtered_data_window_size" in self.filter_parameters

    @abstractmethod
    def apply(self, raw_data, filtered_data):
        """
        The method applies the filters to the raw data.
        :param raw_data: sequence of raw data, the recent data is assumed to be at its end
        :param filtered_data: sequence of filtered data
        :return: filtered data point
        """
        pass

class MovingAverage1D(Filters):
    """
    The class implements the moving average filter. The additional parameters for the class is
    weights for the moving average filter.
    """
    def __init__(self, filter_parameters: dict[str, Any]):
        super().__init__(filter_parameters)
        assert "weights" in self.filter_parameters, "Weights parameters not found"
        assert type(self.filter_parameters["weights"]) == list, "Weights parameters must be a list"
        assert len(self.filter_parameters["weights"]) == self.filter_parameters["raw_data_window_size"], \
            "Weights parameters not found"
        for weight in self.filter_parameters["weights"]:
            assert type(weight) == float, "Weights parameter must be a float"
        self.weights = [w / sum(self.filter_parameters["weights"]) for w in self.filter_parameters["weights"]]

    def apply(self, raw_data, filtered_data):
        if len(raw_data) < len(self.weights):
            return raw_data[-1]
        reversed_raw_data = list(reversed(raw_data))
        output = sum([w * d for w, d in zip(self.weights, reversed_raw_data)])
        return output