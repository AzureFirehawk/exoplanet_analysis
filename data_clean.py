"""
Docstring for data_clean.py

Purpose: Prepare exoplanet data for analysis. Includes unit conversions,
handling missing values , and creation of data subsets.

Module does NOT perform any statistical analysis or visualization.
"""

# imports
import pandas as pd

# constants
PARSEC_TO_LY = 3.26156
COLUMNS_TO_DROP = ["default_flag", "pl_controv_flag", "pl_radelim"]

# -----------------------------
# Cleaning and Aggregation
# -----------------------------
def add_distance_ly(df):
  """
  Add distance in light years to dataframe.
  Rows with missing distance data will have NaN.
  """
  df = df.copy()
  if "sy_dist" not in df.columns:
    print ("Warning: sy_dist column not found in dataframe. Distance data not added.")
    return df

  df["distance_ly"] = df["sy_dist"] * PARSEC_TO_LY
  return df

def add_distance_and_uncertainty_ly(df):
  """
  Add distance and aggregated uncertainty in light years to dataframe.
  If uncertainty data is missing, distance uncertainty will be NaN.
  """
  df = df.copy()
  required_columns = ["sy_dist", "sy_disterr1", "sy_disterr2"]
  if not all (col in df.columns for col in required_columns):
    print ("Warning: Distance uncertainty column not found in dataframe. Skipping uncertainty conversion.")
    return add_distance_ly(df)

  df["distance_ly"] = df["sy_dist"] * PARSEC_TO_LY

  df["distance_uncertainty_ly"] = (
    (df["sy_disterr1"].abs() +
    df["sy_disterr2"].abs()) / 2
  ) * PARSEC_TO_LY
  
  return df

def add_radius_uncertainty(df):
  """
  Add aggregated radius uncertainty column in earth radii to dataframe.
  """
  df = df.copy()
  required_columns = ["pl_rade", "pl_radeerr1", "pl_radeerr2"]
  if not all (col in df.columns for col in required_columns):
    print ("Warning: Radius uncertainty column not found in dataframe. Skipping uncertainty conversion.")
    return df

  df["radius_uncertainty"] = (
    df["pl_radeerr1"].abs() + df["pl_radeerr2"].abs()
  ) / 2
  return df

def drop_columns(df):
  """
  Drop columns from dataframe that are not needed for analysis.
  """
  df = df.copy()
  df = df.drop(columns=COLUMNS_TO_DROP, errors="ignore")
  return df

def prepare_exoplanet_data(df):
  """
  Run necessary data cleaning and aggregation steps.
  """
  df = drop_columns(df)
  df = add_distance_and_uncertainty_ly(df)
  df = add_radius_uncertainty(df)
  return df


# -----------------------------
# Subset Creation
# -----------------------------
def get_planets_with_distance(df):
  """
  Returns a subset of exoplanets with distance data.
  """
  if "distance_ly" not in df.columns:
    raise ValueError("distance_ly column not found in dataframe. Run distance conversion first.")
  
  return df[df["distance_ly"].notna()]

def get_planets_with_radius(df):
  """
  Returns a subset of exoplanets with radius data.
  """
  if "pl_rade" not in df.columns:
    print("Warning: pl_rade column not found.") 
    return pd.DataFrame()
  
  return df[df["pl_rade"].notna()]

def get_planets_with_distance_uncertainty(df):
  """
  Returns a subset of exoplanets with distance uncertainty data.
  """
  required_columns = ["distance_ly", "distance_uncertainty_ly"]
  if not all (col in df.columns for col in required_columns):
    print ("Warning: Distance uncertainty column not found in dataframe. Returning empty dataframe.")
    return pd.DataFrame()
  
  return df[
    df["distance_ly"].notna() & 
    df["distance_uncertainty_ly"].notna()
  ]

def get_planets_with_radius_uncertainty(df):
  """
  Returns a subset of exoplanets with radius uncertainty data.
  """
  required_columns = ["pl_rade", "radius_uncertainty"]
  if not all (col in df.columns for col in required_columns):
    print ("Warning: Radius uncertainty column not found in dataframe. Returning empty dataframe.")
    return pd.DataFrame()
  
  return df[
    df["pl_rade"].notna() & 
    df["radius_uncertainty"].notna()
  ]

# test
if __name__ == "__main__":
    from data_load import load_exoplanet_data

    df_raw = load_exoplanet_data()

    df_clean = prepare_exoplanet_data(df_raw)

    df_dist_unc = get_planets_with_distance_uncertainty(df_clean)
    df_rad_unc = get_planets_with_radius_uncertainty(df_clean)

    print(f"Total planets: {len(df_raw)}")
    print(f"Planets with distance uncertainty: {len(df_dist_unc)}")
    print(f"Planets with radius uncertainty: {len(df_rad_unc)}")

    print("Remaining columns:")
    print(df_clean.columns.tolist())

    print("\nSample distance uncertainty data:")
    print(df_dist_unc[["pl_name", "distance_ly", "distance_uncertainty_ly"]].head())

    print("\nSample radius uncertainty data:")
    print(df_rad_unc[["pl_name", "pl_rade", "radius_uncertainty"]].head())
