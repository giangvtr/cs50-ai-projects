import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from a spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    Evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    evidence = []
    labels = []
    with open(filename) as f:
        # Read the file as a dictionary, where each row is a dictionary with the column headers as keys.
        reader = csv.DictReader(f)
        for row in reader:
            evid_1 = []
            if row["Revenue"] == "TRUE":
                labels.append(1)
            else:
                labels.append(0)
            row["Administrative"] = int(row["Administrative"])
            evid_1.append(row["Administrative"])

            row["Administrative_Duration"] = float(row["Informational"])
            evid_1.append(row["Administrative_Duration"])

            row["Informational"] = int(row["Informational"])
            evid_1.append(row["Informational"])

            row["Informational_Duration"] = float(row["Informational_Duration"])
            evid_1.append(row["Informational_Duration"])

            row["ProductRelated"] = int(row["ProductRelated"])
            evid_1.append(row["ProductRelated"])
            row["ProductRelated_Duration"] = float(row["ProductRelated_Duration"])
            evid_1.append(row["ProductRelated_Duration"])

            row["BounceRates"] = float(row["BounceRates"])
            evid_1.append(row["BounceRates"])
            row["ExitRates"] = float(row["ExitRates"])
            evid_1.append(row["ExitRates"])
            row["PageValues"] = float(row["PageValues"])
            evid_1.append(row["PageValues"])
            row["SpecialDay"] = float(row["SpecialDay"])
            evid_1.append(row["SpecialDay"])

            # Handle month
            month_dict = {
                "Jan": 0, "Feb": 1, "Mar": 2,
                "Apr": 3, "May": 4, "June": 5,
                "Jul": 6, "Aug": 7, "Sep": 8,
                "Oct": 9, "Nov": 10, "Dec": 11,
            }
            row["Month"] = month_dict[row["Month"]]
            evid_1.append(row["Month"])

            row["OperatingSystems"] = int(row["OperatingSystems"])
            evid_1.append(row["OperatingSystems"])

            row["Browser"] = int(row["Browser"])
            evid_1.append(row["Browser"])

            row["Region"] = int(row["Region"])
            evid_1.append(row["Region"])
            row["TrafficType"] = int(row["TrafficType"])
            evid_1.append(row["TrafficType"])

            if row["VisitorType"] == "Returning_Visitor":
                row["VisitorType"] = 1
            else :
                row["VisitorType"] = 0
            evid_1.append(row["VisitorType"])
            if row["Weekend"] == "TRUE":
                row["Weekend"] = 1
            else:
                row["Weekend"] = 0
            evid_1.append(row["Weekend"])
            evidence.append(evid_1)
    return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0
    specificity = 0
    positive = 0
    negative = 0

    for i in range(len(labels)):
        if labels[i] == 1 and predictions[i] == 1:
            sensitivity += 1
        elif labels[i] == 0 and predictions[i] == 0:
            specificity += 1

        if labels[i] == 1: positive += 1
        if labels[i] == 0: negative += 1

    sensitivity /= positive
    specificity /= negative
    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
