"""
Docstring for analysis.py

Purpose: Functions to perform analysis on cleaned exoplanet data for 
answering research questions.
"""

# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Discovery Method Analysis
# -----------------------------

def analyze_discovery_method(df):
  """
  Determine the most common exoplanet discovery methods

  Returns a DataFrame with counts and percentages
  """
  if "discoverymethod" not in df.columns:
    raise ValueError("discoverymethod column not found in dataframe.")
  
  counts = df["discoverymethod"].value_counts()
  total = counts.sum()
  percentages = counts / total * 100

  return pd.DataFrame({
    "Discovery Method": counts.index,
    "Count": counts.values,
    "Percentage": percentages.values
  })

# -----------------------------
# Distance Analysis
# -----------------------------

def analyze_distance_distribution(df, plot=False):
  """
  Analyze the distribution of exoplanet distances (light-years).

  Returns summary statistics.
  """
  distances = df["distance_ly"].dropna().to_numpy()

  stats = {
    "mean": np.mean(distances),
    "median": np.median(distances),
    "min": np.min(distances),
    "max": np.max(distances)
  }

  if plot:
    plt.hist(distances, bins=30)
    plt.xlabel("Distance (light-years)")
    plt.ylabel("Number of planets")
    plt.title("Distribution of Exoplanet Distances")
    plt.show()

  return stats

# -----------------------------
# Planet Size Analysis
# -----------------------------

def analyze_planet_sizes(df):
  """
  Analyze the distribution of exoplanet sizes (Earth radii).

  Returns summary statistics.
  """
  if "pl_rade" not in df.columns:
    raise ValueError("pl_rade column not found in dataframe.")
  
  return df["pl_rade"].dropna().describe()

def categorize_planet_sizes(df):
  """
  Categorize planets by size.
  """
  if "pl_rade" not in df.columns:
    raise ValueError("pl_rade column not found in dataframe.")
  
  radii = df["pl_rade"].dropna().to_numpy()

  categories = {
    "Earth-sized (< 1.25)": np.sum(radii < 1.25),
    "Super-Earth (1.25 - 2.0)": np.sum((radii >= 1.25) & (radii < 2.0)),
    "Neptune-like (2.0 - 6.0)": np.sum((radii >= 2.0) & (radii < 6.0)),
    "Gas Giant (> 6.0)": np.sum(radii >= 6.0)
  }

  return categories

# -----------------------------
# Uncertainty Trend Analysis
# -----------------------------

def analyze_uncertainty_trends(df, uncertainty_column, plot=False):
  """
  Analyze how measurement uncertainty changes over time

  Parameters: 
    df (pandas.DataFrame): DataFrame containing cleaned exoplanet data
    uncertainty_column (str): Name of uncertainty column to analyze
    plot (bool): Whether to plot the mean uncertainty over time

  Returns:
    pandas.DataFrame: DataFrame containing mean uncertainty over time
    plot (matplotlib.pyplot): Plot of mean uncertainty over time
  """
  valid = df[["disc_year", uncertainty_column]].dropna()
  years = valid["disc_year"].to_numpy()
  uncertainties = valid[uncertainty_column].to_numpy()

  unique_years = np.unique(years)
  mean_uncertainty = [
    np.mean(uncertainties[years == year]) 
    for year in unique_years
  ]

  if plot:
    plt.plot(unique_years, mean_uncertainty)
    plt.xlabel("Discovery Year")
    plt.ylabel(f"Mean Uncertainty ({uncertainty_column})")
    plt.title(f"Mean Uncertainty ({uncertainty_column}) Over Time")
    plt.show()

  return pd.DataFrame({
    "disc_year": unique_years,
    "mean_uncertainty": mean_uncertainty
  })

# test

if __name__ == "__main__":
  from data_load import load_exoplanet_data
  from data_clean import (prepare_exoplanet_data)

  df_raw = load_exoplanet_data()
  df_clean = prepare_exoplanet_data(df_raw)

  # Discovery method analysis
  discovery_stats = analyze_discovery_method(df_clean)
  print(discovery_stats)

  # Distance analysis
  distance_stats = analyze_distance_distribution(df_clean, plot=True)
  print("Distance stats:", distance_stats)

  # Planet size analysis
  size_stats = analyze_planet_sizes(df_clean)
  print(size_stats)

  size_categories = categorize_planet_sizes(df_clean)
  print("Size categories:", size_categories)

  # Uncertainty trends
  dist_unc_trends = analyze_uncertainty_trends(
      df_clean,
      "radius_uncertainty",
      plot=True
  )
  print(dist_unc_trends.head())