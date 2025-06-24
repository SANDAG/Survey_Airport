"""
This module provides utility functions for processing SANDAG transportation model loaded networks
    and applying them to the SDIA 2023 Survey data.

It includes functions for opening and manipulating openmatrix files, applying their contents to
    TAZ O-D pairs, and selecting preferred transit types for TAZ O-D pairs.

Functions:
- skim_tod_binning
- open_omx
- extract_skim
- retrieve_skim_value
- get_auto_skim_values
- get_transit_skim_values
- get_total_transit_travel_time
- get_preferred_transit_type
- get_preferred_transit_trip_characteristics

Author: Michael Wehrmeyer
Date: June 2025
"""

# Imports
import numpy as np
import openmatrix as omx
import os
import pandas as pd

tod_list = ['EA','AM','MD','PM','EV','EA']
time_cut = [0,2,8,21,28,44,48]


def skim_tod_binning(
    survey_data: pd.DataFrame
):
    # #### TOD Binning for Respondents
    # https://github.com/SANDAG/ABM/blob/87c3eac743973719d02ffba5b46bb81123e337ac/docs/inputs.md?plain=1#L268
    # - EA = Early morning (3am - 5:59am)<br>
    # - AM = AM peak (6am to 8:59am)<br>
    # - MD = Mid-day (9am to 3:29pm)<br>
    # - PM = PM peak (3:30pm to 6:59pm)<br>
    # - EV = Evening (7pm to 2:59am)<br>

    survey_data.loc[:,'skim_tod'] = (
        pd.cut(
            survey_data['trip_start_time'],
            bins = time_cut,
            right = True,
            include_lowest = True,
            labels = tod_list,
            ordered = False
        )
    )
    return survey_data


def open_omx(
    veh_type:str,
    tod:str,
    base_scenario_path: str
)-> omx.File:
    """
    Navigate to and open skims.

    Args:
        veh_typ (str): 'traffic' or 'transit'
        tod (str): uppercase time-of-day value ('EA','AM','MD','PM','EV')

    Returns:
        omx_file: target skim
    """
    if veh_type not in ('traffic', 'transit') or tod not in ('EA','AM','MD','PM','EV'):
        raise ValueError('Invalid argument for function "open_omx()"')
    skim_path = os.path.join(base_scenario_path,'output','skims',f'{veh_type}_skims_{tod}.omx')
    omx_file = omx.open_file(skim_path, 'r')

    return omx_file


def extract_skim(
    skims:omx.File,
    values: str
)->pd.DataFrame:
    """
    Get skim from omx file (a collection of skims at a specific tod).
    Write skim to a pandas DataFrame
    """
    zones = list(skims.mapping('zone_number').keys())
    df = pd.DataFrame(
        np.array(skims[values]),
        zones,
        zones
    )
    return df


def retrieve_skim_value(
    row: pd.Series,
    skim: pd.DataFrame,
    set_zero_val_to_null:bool = False,
    origin_col:str = 'origin_taz',
    destination_col:str = 'destination_taz'
)-> float:
    """
    Pandas .apply() function that gets skim value for TAZ O-D pairs

    Args:
        skim: matrix of trip characteristics (e.g., distance, transit fare) of TAZ O-D pair
        row: row of values of input skim
        set_zero_val_to_null: 0 values in skims can represent nulls if that trip is unfeasible
                                note that transit travel times are only set to null *after*
                                    summation of all transit trip travel times, so this arg is not used

    """
    value = skim.loc[row[origin_col], row[destination_col]]
    if set_zero_val_to_null and value == 0:
        value = None
    return value


def get_auto_skim_values(
    survey_data: pd.DataFrame,
    base_scenario_path:str
)->pd.DataFrame:
    """
    Gets auto trip characteristics for all survey respondents
    """
    auto_skim_names = ['SOV_NT_M_DIST','SOV_NT_M_TIME','SOV_NT_M_TOLLCOST']
    auto_skim_new_names = ['auto_dist','auto_time','auto_tollcost']
    transit_boarding_index = survey_data['transit_boarding_taz'].notna()

    for tod in tod_list:
        tod_omx_file = open_omx('traffic', tod, base_scenario_path)
        tod_index = (survey_data['skim_tod']==tod)
        for (skim_name, col_name) in zip(auto_skim_names, auto_skim_new_names):
            skim = extract_skim(tod_omx_file, f'{skim_name}__{tod}')
            # get auto skims for all survey respondents
            survey_data.loc[tod_index,col_name] = (
                survey_data
                .loc[tod_index]
                .apply(retrieve_skim_value,
                        skim = skim,
                        set_zero_val_to_null = (col_name in ['auto_dist','auto_time']), # all auto trips must have a distance and time
                        axis = 1)
                )
            # generate comparisons for transit PNROUT ACC times for investigation
            if col_name == 'auto_time':
                survey_data.loc[tod_index * transit_boarding_index,'auto_to_transit_time'] = (
                    survey_data
                    .loc[tod_index * transit_boarding_index]
                    .apply(retrieve_skim_value,
                            skim=skim,
                            destination_col='transit_boarding_taz',
                            set_zero_val_to_null=True,
                            axis=1)
                    )
        tod_omx_file.close()
    return survey_data


transit_access_modes = ['PNROUT','WALK']
transit_flavors = ['LOC','MIX','PRM']
transit_values = ['ACC','FIRSTWAIT','TOTALIVTT','XFERWAIT','EGR','FARE','XFERS']

def get_transit_skim_values(
    survey_data: pd.DataFrame,
    base_scenario_path:str
)->pd.DataFrame:
    """
    Gets walk-to-transit and PNR-to-transit trip characteristics for all survey respondents

    This step takes ~10minutes, could be optimized by only getting skim value for unique TAZ O-D pairs in the survey data,
        and then joining dataframe w/ survey data. This method is not used for lower clarity/lack of significant impact
    """
    for tod in tod_list:
        tod_omx_file = open_omx('transit', tod, base_scenario_path)
        tod_index = (survey_data['skim_tod']==tod)
        for transit_access_mode in transit_access_modes:
            for transit_flavor in transit_flavors:
                transit_mode = f'{transit_access_mode}_{transit_flavor}'.lower()
                survey_data[f'{transit_mode}_time'] = 0.0
                for transit_value in transit_values:
                    col_name = f'{transit_mode}_{transit_value.lower()}'
                    skim = extract_skim(tod_omx_file,f'{col_name.upper()}__{tod}')
                    survey_data.loc[tod_index, col_name] = (
                        survey_data
                        .loc[tod_index]
                        .apply(retrieve_skim_value,
                                skim = skim,
                                origin_col = 'transit_origin_taz',
                                # set_zero_val_to_null = (transit_value=='FARE'), # fares can be $0
                                axis = 1)
                        )
        tod_omx_file.close()
    return survey_data


def get_total_transit_travel_time(
        survey_data: pd.DataFrame
)->pd.DataFrame:
    """
    sum all transit time trip components to get total trip time
    if total transit trip time is 0, make null
    """
    # calculate total transit travel times
    for transit_access_mode in transit_access_modes:
        for transit_flavor in transit_flavors:
            transit_mode = f'{transit_access_mode}_{transit_flavor}'.lower()
            survey_data[f'{transit_mode}_time'] = (
                survey_data[[
                        f'{transit_mode}_acc',
                        f'{transit_mode}_firstwait',
                        f'{transit_mode}_xferwait',
                        f'{transit_mode}_totalivtt',
                        f'{transit_mode}_egr'
                    ]].sum(axis=1)
            )
            # transit trips cannot have 0 trip time
            survey_data.loc[
                    survey_data[f'{transit_mode}_time'] == 0,
                    f'{transit_mode}_time'
                ] = None
    return survey_data


def get_preferred_transit_type(
        survey_data: pd.DataFrame
)->pd.DataFrame:
    """
    Get most time efficient transit type across available options
     - Based on survey respondent access mode
        - Access mode choices, when applied to SANDAG skims, can be WALK or WALK + PNROUT
        - Note that, for survey respondents that did not take transit to the airport, respondents will
            ALWAYS have both access modes available
     - Transit trip types are combinations of access mode (walk vs pnr) & transit flavor (LOC, MIX, PRM)
    """
    walk_transit_cols = ['walk_loc_time','walk_mix_time','walk_prm_time']
    pnr_transit_cols = ['pnrout_loc_time','pnrout_mix_time','pnrout_prm_time']

    def get_transit_type_with_lowest_travel_time(
        access_mode_index: pd.Series,
        transit_time_cols: list
    )-> pd.Series:
        # select column name w/ lowest total travel time of all {transit_time_cols}
        transit_types = (
            survey_data
            .loc[
                access_mode_index,
                transit_time_cols
                ]
            .idxmin(skipna=True, axis=1)
            .str.rsplit('_', n=1, expand = True) # remove '_time' from column string
            [0]
        )
        return transit_types

    # get transit type for respondents that walked to transit
    walk_to_transit_index = (survey_data['access_mode'] == 1)
    survey_data.loc[walk_to_transit_index,'transit_type'] = get_transit_type_with_lowest_travel_time(walk_to_transit_index, walk_transit_cols)

    # get transit type for all other respondents
    not_walk_to_transit_index = (survey_data['access_mode'] != 1)
    survey_data.loc[not_walk_to_transit_index, 'transit_type'] = get_transit_type_with_lowest_travel_time(
        not_walk_to_transit_index,
        walk_transit_cols + pnr_transit_cols
    )

    return survey_data


def get_preferred_transit_trip_characteristics(
        survey_data: pd.DataFrame
        )-> pd.DataFrame:
    """
    Get transit skim times and fares based on optimal transit type
    """
    transit_type_index = survey_data.query('transit_type.notna()').index
    for metric in ['time','fare', 'acc', 'firstwait', 'totalivtt', 'xferwait', 'egr', 'xfers']:
        survey_data.loc[:, f'transit_{metric}'] = (
            survey_data
            .loc[transit_type_index]
            .apply(lambda x: x[f"{x['transit_type']}_{metric}"], axis=1)
        )
    return survey_data
