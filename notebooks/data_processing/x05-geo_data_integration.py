"""
This module:
    - matches survey response coordinates to SANDAG TAZs
    - estimates survey respondent airport trip characteristics for all modes
        - uses SANDAG transportation model loaded network values

Author: Michael Wehrmeyer
Date: June 2025
"""


# Set-up
################################################################################################################################################
import geopandas as gpd
import pandas as pd
import yaml

import os
import sys
sys.path.insert(0, os.path.abspath("./notebooks/data_processing/utils"))
import _geography_matching
import _skim_utils

# input
geography_file = "./data/geographies/TAZ15.shp"
processed_survey_data_path = "./data/processed/data_model_output.csv"
taz_mapping_file_path = './data/geographies/taz_mapping.yaml'
base_scenario_path = r"T:\STORAGE-63T\2025RP_draft\abm_runs_v2\2022_S0_v2"

# output
survey_data_matched_geographies = './data/processed/survey_data_matched_geographies_taz.csv'

# read in data
survey_data = (
    pd.read_csv(processed_survey_data_path)
    .query("validation_severity_person != 'Critical'")
    .query("validation_severity_trip != 'Critical'")
    .query("weight_departing_only > 0")
)
geographies = gpd.read_file(geography_file).query('~TAZ.isin([3,11])') # remove external TAZs that do not exist


# Replace Coordinates w/ Geographies
################################################################################################################################################
# 1) for coords in SD counties ->
#     - match to TAZ
#     - for coords in ocean nearby, match to closest non-external TAZ
# 2) for origin coords outside of SD county:
#     - match closest coord to closest external TAZ

# define limits of SD coast in eps4386 coords
eps4386_coast = {
    'lon': (-117.7,-117.1),
    'lat': (32.535,33.385)
}
max_distance = 100 * 5280 # max distance to external TAZs 100 miles, but in feet

# get TAZs for every geographic type in survey data
for trip_phase in ['origin','destination','home_location','transit_boarding','transit_alighting']:
    survey_data = _geography_matching.match_coordinates_to_internal_taz(survey_data, geographies, trip_phase)
    survey_data = _geography_matching.rescue_adrift_respondents(survey_data, geographies, trip_phase, eps4386_coast)
survey_data = _geography_matching.match_coordinates_to_nearby_external_taz(survey_data, geographies, 'origin', max_distance)
print(f'remaining null origin TAZs: {survey_data['origin_taz'].isnull().sum()}')

# ensure that all responses have origin and destination TAZ
    # TODO insert error statement if lengths do not match
survey_data_init_len = survey_data.shape[0]
survey_data = survey_data.query('(origin_taz.notna()) and (destination_taz.notna())')
print(f'Drops {survey_data_init_len - survey_data.shape[0]} respondents')


# Skims - Auto and Transit
################################################################################################################################################

survey_data = pd.DataFrame(survey_data)

# Adjust Respondent TAZs for Potential Transit Trips
    # many respondents fall just outside PNROUT skims
    # no substantial effect on travel times
with open(taz_mapping_file_path, 'r') as file:
    map_transit_tazs = yaml.safe_load(file)
survey_data['transit_origin_taz'] = survey_data['origin_taz'].replace(map_transit_tazs)

# Read in Loaded Transportation Network Skims
survey_data = _skim_utils.skim_tod_binning(survey_data)
survey_data = _skim_utils.get_auto_skim_values(survey_data, base_scenario_path)
survey_data = _skim_utils.get_transit_skim_values(survey_data, base_scenario_path)

# Get Best Transit Type
survey_data = _skim_utils.get_total_transit_travel_time(survey_data)
survey_data = _skim_utils.get_preferred_transit_type(survey_data)
print(f'Number Respondents w/ Null Transit Type: {survey_data['transit_type'].isna().sum()}') # respondents w/ null transit types are not weighted
survey_data = _skim_utils.get_preferred_transit_trip_characteristics(survey_data)


# Write Out Data
################################################################################################################################################
(
    survey_data
    .to_csv(survey_data_matched_geographies)
)


