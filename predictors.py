from abc import ABC, abstractmethod
import math

from exceptions import OutOfSampleError


class Predictor(ABC):

    def __init__(self, historical_data):
        """
        Store historical DataTable.
        """
        self.historical_data = historical_data
        self.features = historical_data.get_column_names()[:-1]  # Feature1-Feature9
        #[:-1] means all the columns except the last one, which is TumorType

    def check_range(self, patient):
        """
        Raise OutOfSampleError if a feature is outside the historical min/max.
        """
        #pretty much checking if a patient is too differnt from the data
        for f in self.features: #f is just a variable name I chose for “the current feature.” It’s the loop variable:
            low = self.historical_data.get_column_min(f)# finding the lowest value in the historical data for that feature
            high = self.historical_data.get_column_max(f) #finding the highest 
            if patient[f] < low or patient[f] > high: #checking if they are in the range 
                raise OutOfSampleError(f"{f} with value {patient[f]} is outside historical range [{low}, {high}]")
                #
    @abstractmethod #comes from from abc import ABC, abstractmethod
    #it's some kind of decorator that makes sure the method is implemented in the subclasses
        '''from abc import ABC, abstractmethod


    class Animal(ABC):

        @abstractmethod
        def speak(self):
            pass


    class Dog(Animal):

        def speak(self):
            return "Woof"'''

    #Animal is the template: every animal must have a speak method, but it doesn’t say what the sound is. Dog fills it in.
    def predict(self, patient):
        """
        Make a prediction for one patient.
        """
        pass


class MajorityClassPredictor(Predictor):

    def __init__(self, historical_data):
        super().__init__(historical_data) #super() is how a child class calls a method from its parent class. In __init__, 
        #it runs the parent’s 
        #setup code first, so the child gets everything the parent normally creates before adding anything of its own.
        self.majority_class = None #none means that there is nothing in the box yet 
        labels = historical_data.get_column("TumorType") #This pulls out the TumorType column as a list
        if labels.count(1.0) > labels.count(0.0):
            self.majority_class = 1.0
        else:
            self.majority_class = 0.0 #testing if there are more ones or zeros 

    def predict(self, patient):
        """
        Always return the most common historical TumorType.
        """
        self.check_range(patient) #before we do anything we chack if the patient is in the range from before 
        return self.majority_class #either 1.0 or 0.0 


class NearestNeighborPredictor(Predictor):

    def __init__(self, historical_data):
        super().__init__(historical_data)

    def distance(self, patient1, patient2):
        """
        Calculate Euclidean distance using Feature1-Feature9 only.
        """
        total = 0
        for f in self.features:
            total += (patient1[f] - patient2[f]) ** 2 #Euclidean distance formula a number that says how different two patients are.
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