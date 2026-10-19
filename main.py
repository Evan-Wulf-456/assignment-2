
from data_representation import DataTable
from predictors import MajorityClassPredictor, NearestNeighborPredictor
from exceptions import OutOfSampleError


def calculate_accuracy(predictions, actual):
    """Calculate accuracy using only successfully predicted cases."""
    if len(predictions) != len(actual):
        raise ValueError(
            "Predictions and actual lists must have equal lengths."
        )

    matched_predictions = 0
    valid_predictions = 0

    for prediction, actual_label in zip(predictions, actual):
        if prediction is None:
            continue

        valid_predictions += 1

        if prediction == actual_label:
            matched_predictions += 1

    if valid_predictions == 0:
        raise ValueError(
            "Cannot calculate accuracy without valid predictions."
        )

    return matched_predictions / valid_predictions


def main():
    # Load the historical data first.
    historical = DataTable("data/cancer_historical1.csv")

    # Use historical averages to impute missing values in new cases.
    new_cases = DataTable(
        "data/cancer_new_cases1.csv",
        reference=historical
    )

    labels = DataTable("data/cancer_new_cases_labels1.csv")
    actual_labels = labels.get_column("TumorType")

    if len(new_cases.data) != len(actual_labels):
        raise ValueError(
            "The number of new cases must match the number of labels."
        )

    mode_predictor = MajorityClassPredictor(historical)
    nn_predictor = NearestNeighborPredictor(historical)

    mode_predictions = []
    nn_predictions = []

    for i in range(len(new_cases.data)):
        patient = new_cases.get_row(i)

        try:
            mode_prediction = mode_predictor.predict(patient)
        except OutOfSampleError as error:
            print(f"Mode, case {i}: {error}")
            mode_prediction = None

        try:
            nn_prediction = nn_predictor.predict(patient)
        except OutOfSampleError as error:
            print(f"Nearest Neighbor, case {i}: {error}")
            nn_prediction = None

        mode_predictions.append(mode_prediction)
        nn_predictions.append(nn_prediction)

    for name, predictions in [
        ("Mode", mode_predictions),
        ("Nearest Neighbor", nn_predictions),
    ]:
        valid_count = sum(
            prediction is not None for prediction in predictions
        )

        print(
            f"{name} valid predictions: "
            f"{valid_count}/{len(actual_labels)}"
        )

        if valid_count == 0:
            print(f"{name} accuracy: unavailable")
        else:
            accuracy = calculate_accuracy(
                predictions, actual_labels
            )
            print(f"{name} accuracy: {accuracy:.4f}")


if __name__ == "__main__":
    main()
