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

# imports
from data_load import load_exoplanet_data
from data_clean import prepare_exoplanet_data
from analysis import (
  analyze_discovery_method, 
  analyze_distance_distribution, 
  analyze_planet_sizes,
  categorize_planet_sizes,
  analyze_uncertainty_trends
)
from spinner import spinner

# configuration
SHOW_PLOTS = True

# main
def main():
  print("Loading exoplanet data...")
  df_raw = load_exoplanet_data()
  spinner()
  print("Preparing data for analysis...")
  df = prepare_exoplanet_data(df_raw)
  spinner()

  print(f"Total exoplanets in dataset: {len(df)}")

  print("\nPerforming analysis...")
  spinner()

  # ---------------------------------
  # Question 1: Discovery Methods
  # ---------------------------------
  print("\nQuestion 1: What is the most common method used to find exoplanets?")

  spinner()
  print("\nDiscovery method statistics:")
  discovery_stats = analyze_discovery_method(df)
  print(discovery_stats.head())

  # ---------------------------------
  # Question 2: Distance Analysis
  # ---------------------------------
  print("\nQuestion 2: Is it more common to find closer or more distant planets?")

  spinner()
  print("\nDistance statistics (light-years):")
  distance_stats = analyze_distance_distribution(df, plot=SHOW_PLOTS)
  for key, value in distance_stats.items():
    print(f"{key}: {value:.2f}")

  # ---------------------------------
  # Question 3: Planet Size Analysis
  # ---------------------------------
  print("\nQuestion 3: How large are the planets we're finding?")

  spinner()
  print("\nPlanet size statistics (Earth radii):")
  size_stats = analyze_planet_sizes(df)
  print(size_stats)

  print("\nPlanet size categories:")
  size_categories = categorize_planet_sizes(df)
  for category, count in size_categories.items():
    print(f"{category}: {count} planets")

  # ---------------------------------
  # Question 4: Uncertainty Trends
  # ---------------------------------
  print("\nQuestion 4: How has our accuracy/uncertainty changed over the years?")

  spinner()
  print("\nDistance uncertainty trends:")
  dist_unc_trends = analyze_uncertainty_trends(
    df, 
    "distance_uncertainty_ly", 
    plot=SHOW_PLOTS
  )
  print(dist_unc_trends)

  print("\nRadius uncertainty trends:")
  rad_unc_trends = analyze_uncertainty_trends(
    df, 
    "radius_uncertainty", 
    plot=SHOW_PLOTS
  )
  print(rad_unc_trends)

if __name__ == "__main__":
  main()