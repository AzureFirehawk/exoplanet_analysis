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