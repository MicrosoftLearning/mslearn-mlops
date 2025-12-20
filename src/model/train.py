# Import libraries

import argparse
import glob
import logging
import os

import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# define functions
def main(args):
    # enable MLflow autologging and basic logging
    # use the generic autolog() so MLflow picks the appropriate autologger
    mlflow.autolog()
    logging.basicConfig(level=logging.INFO)

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


def split_data(df, test_size: float = 0.2, random_state: int = 123):
    """Split a dataframe into train/test sets.

    This function attempts to infer the target column. If a column named
    'Diabetic' (case-sensitive) exists it will be used as the label. If not,
    the last column is used as the label. Patient identifiers like 'PatientID'
    are dropped when present.
    """
    # choose target
    if 'Diabetic' in df.columns:
        y = df['Diabetic']
        X = df.drop(['Diabetic', 'PatientID'], axis=1, errors='ignore')
    elif 'diabetic' in df.columns:
        y = df['diabetic']
        X = df.drop(['diabetic', 'PatientID'], axis=1, errors='ignore')
    else:
        y = df.iloc[:, -1]
        X = df.iloc[:, :-1]

    # perform train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    return X_train, X_test, y_train, y_test


def train_model(reg_rate, X_train, X_test, y_train, y_test):
    # train model
    # log parameters using standard logging; MLflow autolog will also capture
    logging.info(f"Training model with reg_rate={reg_rate}")

    with mlflow.start_run():
        model = LogisticRegression(C=1 / reg_rate, solver="liblinear")
        model.fit(X_train, y_train)

        # evaluate
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)

        # record metrics to both logging and MLflow (MLflow autolog captures this too)
        logging.info(f"Model accuracy: {acc}")
        mlflow.log_metric("accuracy", float(acc))

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
