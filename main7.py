from data_representation import DataTable
from predictors import MajorityClassPredictor, NearestNeighborPredictor
from exceptions1 import OutOfSampleError


def calculate_accuracy(predictions, actual):
    if len(predictions) == 0:
        raise ValueError("Cannot divide by zero.")
    if len(predictions) != len(actual):
        raise ValueError("Predictions and actual lists must have equal lengths")
     
    matched_predictions = 0 # initialize the matched predictions to 0 
    for prediction, actual_label in zip(predictions, actual): # extract the individual values of the predictions and actual list 
        if prediction == actual_label: # if the prediction matches the actual value, then increment the matched prediction by one 
            matched_predictions += 1 
    accuracy = matched_predictions / len(predictions) # after incrementing the matched predictions, calculate the predictions that matched over the total amount of predictions. If the counted predictions is close to the total amount of predictions in the dataset, then accuracy is high. Otherwise, accuracy is low. 
        

    return accuracy # give the variable or the result of the calculation back to the function 
    
    

def main():

    # Load datasets
    historical = DataTable("Data/cancer_historical.csv")
    new_cases = DataTable("Data/cancer_new_cases.csv")
    labels = DataTable("Data/cancer_new_cases_labels.csv")


    # Create predictors
    mode_predictor = MajorityClassPredictor(historical)
    nn_predictor = NearestNeighborPredictor(historical)


    mode_predictions = []
    nn_predictions = []


    # Predict every new case
    for i in range(len(new_cases.data)):

        patient = new_cases.get_row(i)

        try:
            mode_predictions.append(
                mode_predictor.predict(patient)
            )

            nn_predictions.append(
                nn_predictor.predict(patient)
            )

        except OutOfSampleError as e:
            print(e)


    # Get true labels
    actual_labels = labels.get_column("TumorType")


    # Accuracy
    print(
        "Mode accuracy:",
        calculate_accuracy(mode_predictions, actual_labels)
    )

    print(
        "Nearest Neighbor accuracy:",
        calculate_accuracy(nn_predictions, actual_labels)
    )


if __name__ == "__main__":
    main()