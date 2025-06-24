"""
This module provides utility functions for matching SDIA 2023 Survey coordinates to SANDAG TAZs.

Functions:
- make_survey_geodataframe
- transform_geographies_df
- match_coordinates_to_internal_taz
- rescue_adrift_respondents
- match_coordinates_to_nearby_external_taz

Author: Michael Wehrmeyer
Date: June 2025
"""

# Imports
import geopandas as gpd
import pandas as pd

survey_crs = "EPSG:4326"


def make_survey_geodataframe(
    survey_df: pd.DataFrame,
    trip_phase:str
)->gpd.GeoDataFrame:
    """
    Converts Survey data pandas dataframe into geopandas geo-dataframe
    Args:
        - survey_df: survey responses
        - trip_phase: prefix to the coordinate columns in the survey data to build geodataframe off of
            - geodataframe requires one "geometry" column
    """
    survey_gdf =gpd.GeoDataFrame(
                survey_df,
                geometry=gpd.points_from_xy(
                    survey_df[f"{trip_phase}_longitude"],
                    survey_df[f"{trip_phase}_latitude"]
                ),
                crs=survey_crs,
            )
    return survey_gdf


def transform_geographies_df(
    geography_gdf:gpd.GeoDataFrame,
    trip_phase:str
)->gpd.GeoDataFrame:
    """
    Prepares TAZ geodataframe for comparison w/ survey respondent coordinates
        (helper function)
    """
    geography_gdf = (
            geography_gdf
            [['TAZ', "geometry"]]
            .rename(columns={'TAZ':f'{trip_phase}_taz'})
        )
    return geography_gdf


def match_coordinates_to_internal_taz(
    survey_df:pd.DataFrame,
    geography_gdf:gpd.GeoDataFrame,
    trip_phase:str
)->gpd.GeoDataFrame:
    """
    Spatial join assigning coordinates to internal TAZs that they sit inside of
        - Coordinate columns specified by 'trip_phase'
        - Does not match to external TAZ bc external TAZs are points
    """
    geography_gdf = transform_geographies_df(geography_gdf, trip_phase)
    survey_gdf = make_survey_geodataframe(survey_df, trip_phase)
    survey_gdf = (
        survey_gdf
        .to_crs(geography_gdf.crs)
        .sjoin(geography_gdf, how="left")
        .astype({f"{trip_phase}_taz": "Int32"})
        .drop(columns=['index_right'])
    )
    survey_gdf.columns = [col.lower() for col in survey_gdf.columns]
    return survey_gdf


def rescue_adrift_respondents(
    survey_df:pd.DataFrame,
    geography_gdf:gpd.GeoDataFrame,
    trip_phase:str,
    eps4386_coast: dict
)->gpd.GeoDataFrame:
    """
    Some respondents gave coordinates that were placed just off of the SD Coast
        This function matches their given coordinates with the nearest TAZ
    Args:
        - eps4386_coast: dictionary defining the bounds of the SD coast close to the land
            - uses eps4386 coordinate system
    """
    geo_col = f"{trip_phase}_taz"
    geography_gdf = transform_geographies_df(geography_gdf, trip_phase)
    survey_gdf = make_survey_geodataframe(survey_df, trip_phase)

    adrift_respondents_index = (
        survey_gdf
            .query(f'{geo_col}.isnull()')
            .loc[survey_gdf[f'{trip_phase}_latitude'].between(eps4386_coast['lat'][0],eps4386_coast['lat'][1])]
            .loc[survey_gdf[f'{trip_phase}_longitude'].between(eps4386_coast['lon'][0],eps4386_coast['lon'][1])]
            .index
    )
    print(f'num adrift respondents: {adrift_respondents_index.shape}')

    survey_gdf.loc[
        adrift_respondents_index,
        geo_col
    ] = (
            survey_gdf
            .loc[adrift_respondents_index,'geometry']
            .reset_index(drop=False)
            .rename(columns={'index':'adrift_index'})
            .to_crs(geography_gdf.crs)
            .sjoin_nearest(geography_gdf, how="left", max_distance = 100000)
            .set_index('adrift_index')
            .astype({geo_col: "Int32"})
            [geo_col]
            .values
    )

    survey_gdf.columns = [col.lower() for col in survey_gdf.columns]
    return survey_gdf


def match_coordinates_to_nearby_external_taz(
    survey_df:pd.DataFrame,
    geography_gdf:gpd.GeoDataFrame,
    trip_phase:str,
    max_distance: int
)->gpd.GeoDataFrame:
    """
    Many respondents have travel origins outside of the SD County
        This function matches these respondents to their nearest SANDAG External TAZ

    Respondents that are too far from SD County are not matched
        Respondents considered 'too far' using some defined max_distance
    """
    geo_col = f"{trip_phase}_taz"

    external_tazs_df = transform_geographies_df(geography_gdf.query('TAZ <= 12'), trip_phase)
    external_tazs_df['geometry'] = external_tazs_df['geometry'].centroid
    external_tazs_df = gpd.GeoDataFrame(external_tazs_df)

    survey_gdf = make_survey_geodataframe(survey_df, trip_phase)

    missing_taz_index = (
        survey_df
        .query(f'{geo_col}.isnull()')
        .index
    )
    print(f'num respondents w/ {trip_phase} outside of county: {missing_taz_index.shape}')

    closest_geographies = (
        survey_gdf
        .loc[missing_taz_index, 'geometry']
        .reset_index(drop=False)
        .rename(columns={'index':'missing_index'})
        .to_crs(external_tazs_df.crs)
        .sjoin_nearest(external_tazs_df, how="left", distance_col= 'distance_between_points')
        .groupby(['missing_index', geo_col])
        ['distance_between_points']
        .min()
        .reset_index(drop=False)
        .set_index('missing_index')
        .astype({geo_col: "Int32"})
    )
    survey_gdf.loc[missing_taz_index,geo_col]=(
        closest_geographies
        .where(
            closest_geographies['distance_between_points'] < max_distance,
            None
        )
        [geo_col]
    )

    survey_gdf.columns = [col.lower() for col in survey_gdf.columns]
    return survey_gdf
