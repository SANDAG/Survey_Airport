"""
Utility functions used with the data model.
"""

from collections import defaultdict
from typing import Any, get_origin, get_args, Annotated, Optional
from enum import Enum, IntEnum

def extract_base_type(typ):
    """
    Extracts base type from complex annotations. This is needed to identify whether a variable 
    is an Enum. Without this step, the origin of all the variables in the model is Annotated, even the variable is an Enum
    """
    origin = get_origin(typ)
    if origin is not Enum:      
        base = get_args(typ)
        if base:
           base = extract_base_type(base[0])
           return base
    return typ


def add_enum_label_columns(df,model):
    """
    After the datamodel output is converted into a dataframe, this method adds a column to the output dataframe for each Enum variable in the datamodel. This column 
    shows the Enum label.
    """
    
    for field, field_type in model.__annotations__.items():
        base_type = extract_base_type(field_type)
        if issubclass(base_type,(Enum,IntEnum)):
            enum_names = {item.value: item.name for item in base_type}
            enum_name_col = f"{field}_label" 
            df[enum_name_col] = df[field].map(enum_names).astype(str)
    return df


def add_list_objects(
    child_list: list,
    child_key: str,
    parent_list: list,
    parent_key: str,
    parent_variable: str,
) -> list:
    """
    Maps a list of child objects to a list of parent objects. The child objects
    are added to the parent objects as a list using the `parent_variable` as the
    key. The `child_key` is used to match the child to the parent using the
    `parent_key`.
    """
    parent_to_child_map = defaultdict(dict)
    for child in child_list:
        temp_key = child[child_key]
        del child[child_key]
        parent_to_child_map[temp_key] = child

    for parent in parent_list:
        temp_key = parent[parent_key]
        parent[parent_variable] = parent_to_child_map.get(temp_key, {})

    return parent_list


def nan_to_none(cls, value: Any):
    """
    Convert nan to none to address that missing strings were being read as nan, which resulted in a value error when using using Optional[str]
    """
    if value != value:
        return None
    return value


def military_to_clock(military_time):
    """Converts a military time string (HHMM) to a 12-hour clock format string (hh:mm AM/PM).

    Args:
        military_time: A string representing time in 24-hour format (e.g., "0600").

    Returns:
        A string representing time in 12-hour clock format (e.g., "6:00 AM").

    Raises:
        ValueError: If the input string is not in the correct format (HHMM).
    """

    if not military_time.isdigit() or len(military_time) != 4:
        raise ValueError(
            "Invalid military time format. Please use HHMM format (e.g., 0600)."
        )

    hours = int(military_time[:2])
    minutes = int(military_time[2:])

    # Convert to 12-hour format
    if hours == 0:
        clock_hours = 12
        period = "am"
    elif hours >= 12:
        clock_hours = hours - 12
        period = "pm"
    else:
        clock_hours = hours
        period = "am"

    # Format the output string
    return f"{clock_hours:02d}:{minutes:02d} {period}"
