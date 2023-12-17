# Import libraries

import argparse
import glob
import os

import mlflow
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


# define functions
def main(args):
    # enable autologging
    mlflow.autolog()

    # read data
    df = get_csvs_df(args.training_data)

    # split data
    X_train, X_test, y_train, y_test = split_data(df)

    # train model
    train_model(args.reg_rate, X_train, X_test, y_train, y_test)


def get_csvs_df(path):
    if not os.path.exists(path):
        raise RuntimeError(f"Cannot use non-existent path provided: {path}")
    csv_files = glob.glob(f"{path}/*.csv")
    if not csv_files:
        raise RuntimeError(f"No CSV files found in provided data path: {path}")
    return pd.concat((pd.read_csv(f) for f in csv_files), sort=False)


# TO DO: add function to split data


def train_model(reg_rate, X_train, X_test, y_train, y_test):
    # train model
    LogisticRegression(C=1/reg_rate, solver="liblinear").fit(X_train, y_train)


def parse_args() -> argparse.Namespace:
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


def split_data(
        df: pd.DataFrame,
        test_size: float = 0.2,
        random_state: int = 42,
        feature_cols: list = None,
        label_col: str = None,
):
    """

    Split Data

    Function for splitting a dataframe into training and testing datasets.

    Args:
        df: The input dataframe.
        test_size: The proportion of the data to include in the testing
         dataset. Defaults to 0.2.
        random_state: The seed used by the random number generator. Defaults
         to 42.
        feature_cols: The list of column names to use as features. If not
         provided, the default features are ['Pregnancies', 'PlasmaGlucose',
         'DiastolicBloodPressure', 'TricepsThickness', 'SerumInsulin', 'BMI',
         'DiabetesPedigree', 'Age'].
        label_col: The name of the column to use as the label. If not provided,
         the default label is 'Diabetic'.

    Returns:
        A tuple containing the training features, testing features, training
        labels, and testing labels.

    Example usage:

    >>> X_train, X_test, y_train, y_test = split_data(
    >>>     df,
    >>>     test_size=0.3,
    >>>     random_state=10,
    >>>     feature_cols=['Age', 'BMI'],
    >>>     label_col='Diabetic'
    >>> )

    """

    if feature_cols is None:
        feature_cols = [
            'Pregnancies',
            'PlasmaGlucose',
            'DiastolicBloodPressure',
            'TricepsThickness',
            'SerumInsulin',
            'BMI',
            'DiabetesPedigree',
            'Age'
        ]

    if label_col is None:
        label_col = "Diabetic"

    # select relevant columns
    df = df[feature_cols + [label_col]]

    # split into feature and label array
    X = df[feature_cols].values
    y = df[label_col].values

    # perform train test split
    return train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )


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
