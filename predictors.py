from abc import ABC, abstractmethod
import math

from exceptions1 import OutOfSampleError


class Predictor(ABC):

    def __init__(self, historical_data):
        """
        Store historical DataTable.
        """
        self.historical_data = historical_data
        self.features = historical_data.get_column_names()[:-1]  # Feature1-Feature9

    def check_range(self, patient):
        """
        Raise OutOfSampleError if a feature is outside the historical min/max.
        """
        for f in self.features:
            low = self.historical_data.get_column_min(f)
            high = self.historical_data.get_column_max(f)
            if patient[f] < low or patient[f] > high:
                raise OutOfSampleError(
                    f"{f} with value {patient[f]} is outside historical range [{low}, {high}]"
                )

    @abstractmethod
    def predict(self, patient):
        """
        Make a prediction for one patient.
        """
        pass


class MajorityClassPredictor(Predictor):

    def __init__(self, historical_data):
        super().__init__(historical_data)
        self.majority_class = None
        labels = historical_data.get_column("TumorType")
        if labels.count(1.0) > labels.count(0.0):
            self.majority_class = 1.0
        else:
            self.majority_class = 0.0

    def predict(self, patient):
        """
        Always return the most common historical TumorType.
        """
        self.check_range(patient)
        return self.majority_class


class NearestNeighborPredictor(Predictor):

    def __init__(self, historical_data):
        super().__init__(historical_data)

    def distance(self, patient1, patient2):
        """
        Calculate Euclidean distance using Feature1-Feature9 only.
        """
        total = 0
        for f in self.features:
            total += (patient1[f] - patient2[f]) ** 2
        return math.sqrt(total)

    def predict(self, patient):
        """
        Find closest historical patient and return its TumorType.
        """
        self.check_range(patient)
        best_distance = None
        best_label = None
        for i in range(len(self.historical_data.data)):
            other = self.historical_data.get_row(i)
            d = self.distance(patient, other)
            if best_distance is None or d < best_distance:
                best_distance = d
                best_label = other["TumorType"]
        return best_label