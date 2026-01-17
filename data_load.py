"""
Docstring for data_load.py

Purpose: Load raw data from NASA Exoplanet Archive into
a pandas dataframe and perform basic validation of the data.

Module does NOT perform any data cleaning, unit conversion, or analysis.
"""
# imports
import pandas as pd
import os

# constants/config
DEFAULT_DATA_PATH = "data/exoplanet_archive.csv"

REQUIRED_COLUMNS = [
  "pl_name",
  "discoverymethod",
  "disc_year"
]

OPTIONAL_COLUMNS = [
  "sy_dist",
  "sy_disterr1",
  "sy_disterr2",
  "pl_rade",
  "pl_radeerr1",
  "pl_radeerr2",
  "pl_radelim"
]

# validation
def validate_file_exists(filepath):
  """
  Check if file exists.
  """
  if not os.path.exists(filepath):
    raise FileNotFoundError(f"File does not exist: {filepath}")

def validate_columns(df):
  """
  Check if required columns are present.
  """
  missing_required = [col for col in REQUIRED_COLUMNS if col not in df.columns]
  if missing_required:
    raise ValueError(f"Missing required columns: {missing_required}")

  missing_optional = [col for col in OPTIONAL_COLUMNS if col not in df.columns]
  if missing_optional:
    print(f"Warning: Optional columns missing: {missing_optional}")

# load data
def load_exoplanet_data(filepath=DEFAULT_DATA_PATH):
  """
  Load raw data from CSV file into a pandas dataframe.

  Parameters:
    filepath (str): Path to CSV file containing exoplanet data.

  Returns:
    pandas.DataFrame: Dataframe containing exoplanet data.
  """
  validate_file_exists(filepath)
  df = pd.read_csv(
    filepath,
    comment = "#",
    sep = ",",
    engine = "python"
  )
  validate_columns(df)
  return df

# inspect
def print_basic_info(df):
  """
  Print basic information about the dataframe.
  """
  print("Dataset loaded successfully")
  print(f"Number of rows: {df.shape[0]}")
  print(f"Number of columns: {df.shape[1]}")
  print("\nColumns:")
  print(df.columns.tolist())


# test
if __name__ == "__main__":
  df = load_exoplanet_data()
  print_basic_info(df)
  print("\nFirst 5 rows:")
  print(df.head())
