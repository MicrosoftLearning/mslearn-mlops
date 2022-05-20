# Import libraries
import argparse
import glob
from pathlib import Path
import pandas as pd
import mlflow

def main():

    # Log row count of input data
    row_count = (len(df))
    mlflow.log_metric('row count input data', row_count)


def load_data(data_path)
    
    # Load the data folder (passed as input dataset)
    all_files = glob.glob(data_path + "/*.csv")
    df = pd.concat((pd.read_csv(f) for f in all_files), sort=False)

def remove_nulls(loaded_data)

# get parameters
parser = argparse.ArgumentParser()
parser.add_argument("--input_data", type=str, help='Path to input data')
parser.add_argument('--output_data', type=str, help='Path of output data')
args = parser.parse_args()

\

# remove nulls
df = df.dropna()

# log processed rows
row_count_processed = (len(df))
mlflow.log_metric('row count output data', row_count_processed)

# set the processed data as output
output_df = df.to_csv((Path(args.output_data) / "output_data.csv"))