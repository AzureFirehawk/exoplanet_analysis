"""
Docstring for main.py

Purpose: Main entry point for the program. Combines the loading, cleaning,
and analysis modules to fully analyze the exoplanet data and answer four 
questions:

Questions:
-What is the most common method used to find exoplanets? 
-Is it more common to find closer or more distant planets? 
-How large are the planets we're finding? 
-How has our accuracy/uncertainty changed over the years?
"""

from data_load import load_exoplanet_data
from data_clean import prepare_exoplanet_data
from analysis import (
  analyze_discovery_method, 
  analyze_distance_distribution, 
  analyze_planet_sizes,
  categorize_planet_sizes,
  analyze_uncertainty_trends
)

# configuration
SHOW_PLOTS = True

# main
def main():
  print("Loading exoplanet data...")
  df_raw = load_exoplanet_data()
  print("Preparing data for analysis...")
  df = prepare_exoplanet_data(df_raw)

  print(f"Total exoplanets in dataset: {len(df)}")

  # ---------------------------------
  # Question 1: Discovery Methods
  # ---------------------------------
  print("\nQuestion 1: What is the most common method used to find exoplanets?")

  discovery_stats = analyze_discovery_method(df)
  print(discovery_stats.head())

  # ---------------------------------
  # Question 2: Distance Analysis
  # ---------------------------------
  print("\nQuestion 2: Is it more common to find closer or more distant planets?")

  distance_stats = analyze_distance_distribution(df, plot=SHOW_PLOTS)
  for key, value in distance_stats.items():
    print(f"{key}: {value:.2f}")

  # ---------------------------------
  # Question 3: Planet Size Analysis
  # ---------------------------------
  print("\nQuestion 3: How large are the planets we're finding?")

  print("\nPlanet size statistics (Earth radii):")
  size_stats = analyze_planet_sizes(df)
  print(size_stats)

  print("\nPlanet size categories:")
  size_categories = categorize_planet_sizes(df)
  for category, values in size_categories.items():
    print(f"{category}: {len(values)} planets")

  # ---------------------------------
  # Question 4: Uncertainty Trends
  # ---------------------------------


if __name__ == "__main__":
  main()