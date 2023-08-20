# Import libraries

import argparse
import glob
import os

import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn

# define functions
def main(args):
    # TO DO: enable autologging

    mlflow.start_run()       

    # read data
    df = get_csvs_df(args.training_data)

    # split data
    X_train, X_test, y_train, y_test = split_data(df)

    # train model
    model = train_model(args.reg_rate, X_train, X_test, y_train, y_test)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    # Log metrics or other information
    mlflow.log_metric('accuracy', accuracy)

    # End run 
    mlflow.end_run()



def get_csvs_df(path):
    if not os.path.exists(path):
        raise RuntimeError(f"Cannot use non-existent path provided: {path}")
    csv_files = glob.glob(f"{path}/*.csv")
    if not csv_files:
        raise RuntimeError(f"No CSV files found in provided data path: {path}")
    return pd.concat((pd.read_csv(f) for f in csv_files), sort=False)


# TO DO: add function to split data
def split_data(df, test_size=0.2, random_state=None):
    """
    Split the data into training and testing sets.
    
    Parameters:
        X (array-like): Features or input data.
        y (array-like): Target variable or labels.
        test_size (float): The proportion of the dataset to include in the test split.
        random_state (int or RandomState instance): Controls the shuffling applied to the data before splitting.
    
    Returns:
        X_train (array-like): Training features.
        X_test (array-like): Testing features.
        y_train (array-like): Training target variable.
        y_test (array-like): Testing target variable.
    """
    features = df.drop(columns=["Diabetic"])

    X_train, X_test, y_train, y_test = train_test_split(features, "Diabetic", test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

def train_model(reg_rate, X_train, X_test, y_train, y_test):
    # train model
    model = LogisticRegression(C=1/reg_rate, solver="liblinear").fit(X_train, y_train)
    return model


def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--training_data", dest='training_data',
                        type=str)
    parser.add_argument("--reg_rate", dest='reg_rate',
                        type=float, default=0.01)

    # parse args
    args = parser.parse_args()

    # return args
    return args

# run script
if __name__ == "__main__":
    # add space in logs
    print("\n\n")
    print("*" * 60)

    # parse args
    args = parse_args()

    # run main function
    main(args)

    # add space in logs
    print("*" * 60)
    print("\n\n")
