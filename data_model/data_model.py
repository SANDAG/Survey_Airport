"""
Data Model for the SDIA Survey
"""

from datetime import datetime, time
from math import isnan
from typing import Annotated, Any, ClassVar, Literal, Optional, TypeVar, Union, List

from pydantic import (BaseModel, BeforeValidator, Field, computed_field,
                      field_validator, model_validator)
from pydantic_extra_types.coordinate import Coordinate, Latitude, Longitude
import pandas as pd
import enums as e
import re


def coerce_nan_to_none(x: Any, field_name: str) -> Any:
    try:
        if isinstance(x, (float, int)) and isnan(x):
            return None
    except TypeError as e:
        # Print or log the problematic field and its value
        print(f"Error in field '{field_name}' with value: {x}")
        raise e  # Re-raise the exception for debugging
    return x


def coerce_nan_string_to_none(x: Any) -> Any:
    if x != x:
        return None
    return x


T = TypeVar("T")

NoneOrNan = Annotated[Optional[T], BeforeValidator(coerce_nan_to_none)]
NoneOrNanString = Annotated[Optional[T], BeforeValidator(coerce_nan_string_to_none)]


class SkipLogicValidator:
    def __init__(self, skip_logic_csv):
        self.rules = pd.read_csv(skip_logic_csv)
    
    def get_rules_for_class(self, class_name):
        """Filter skip logic rules for a specific class."""
        return self.rules[self.rules['class'] == class_name]
    
    def validate(self, class_name, data):
        """Validate data using skip logic rules for a specific class."""
        errors = []
        severity_levels = {"Non-Critical" : 0, "Critical": 0}  # Track severity levels
        
        rules = self.get_rules_for_class(class_name)
        
        for _, rule in rules.iterrows():
            # Extract rule details
            condition_variable = rule['condition_variable']
            condition_values = str(rule['condition_value']).split(',')  # Ensure it's a string before splitting
            check_type = rule['check_type']
            check_variables = rule['check_variables'].split(',')
            check_values = str(rule['check_values']).split(',') if pd.notna(rule['check_values']) else []
            severity = rule['severity']
            
            # Perform validation based on check_type
            if check_type == "critical":
                # Check fields directly for missing values
                if self.perform_critical_check(data, check_variables):
                    errors.append(f"{', '.join(check_variables)}: {severity}")
                    severity_levels[severity] += 1

            elif check_type == "missing":
                # Conditional validation allowing multiple condition values
                if condition_variable in data and str(data[condition_variable]) in condition_values:
                    if not self.perform_check(data, check_type, check_variables, check_values):
                        errors.append(f"{', '.join(check_variables)}: {severity}")
                        severity_levels[severity] += 1
                        
            elif check_type == "value":
                # Perform a value check even if no condition_variable is given
                if not condition_variable or (condition_variable in data and str(data[condition_variable]) in condition_values):
                    if not self.perform_check(data, check_type, check_variables, check_values):
                        errors.append(f"{', '.join(check_variables)}: {severity}")
                        severity_levels[severity] += 1
        
        return errors, severity_levels, len(errors)
    
    def perform_critical_check(self, data, check_variables):
        """
        Check if any of the critical fields are missing.
        Returns True if any field is missing, False otherwise.
        """
        for var in check_variables:
            if var not in data or data[var] is None:
                # Log which variable failed the critical check
                print(f"Critical check failed for variable: {var}")
                return True  # A missing field causes the critical check to fail
        return False  # All fields are present
    
    def perform_check(self, data, check_type, check_variables, check_values):
        """Perform the validation check based on the check_type."""
        if check_type == "missing":
            # Return False if any of the variables are missing
            return all(var in data and data[var] is not None for var in check_variables)
        elif check_type == "value":
            # Return False if any of the variables do not match the expected values
            return all(var in data and data[var] in check_values for var in check_variables)
        return True



skip_logic_validator = SkipLogicValidator("../data/processed/skip_logic.csv")


class PydanticModel(BaseModel):
    """
    Base class for all Pydantic models, create in case future modifications are helpful
    """

    # valid_record: bool = Field(
    #     default=True, description="Indicates if the record is valid")
    # """
    # Indicates if the record is valid
    # """

    validation_error: str = Field(
        default="", description="Holds validation error messages")
    """
    Holds the validation error message
    """

    validation_severity: str = Field(
        default = "", description = "Holds the severity of the validation error"
    )
    """
    Holds the severity of the validation error
    """

    validation_num_errors: int = Field(
        default = 0, description = "Number of missing (null) fields for the record"
    )
    """
    Number of missing (null) fields for the record
    """

    @model_validator(mode="before")
    def check_validation_of_numeric_value(cls, values):
        # List of fields to validate
        fields_to_check = ['taxi_fhv_fare', 'taxi_fhv_wait', 'parking_cost']
        
        for field in fields_to_check:
            value = values.get(field)
            if isinstance(value, datetime):
                values[field] = value.strftime('%Y-%m-%d %H:%M:%S') #change to pass through the data model anyway
                #values['valid_record'] = False
                values['validation_severity'] = "Low"
                values['validation_error'] = f"{field} is datetime"

        return values




class Lat(BaseModel):
    lat: Latitude
    """Latitude"""

class Lng(BaseModel):
    lng: Longitude
    """Longitude"""

class Coord(BaseModel):
    coord: Coordinate

class Trip(PydanticModel):
    """
    Data model for a trip taken by a respondent.
    """

    inbound_or_outbound: NoneOrNan[e.InboundOutbound] = Field(
        ...,
        description="Whether the trip is inbound to the airport or outbound from the airport",
    )
    """
    Whether the trip is inbound to the airport or outbound from the airport.
    """

    origin_activity_type: NoneOrNanString[e.ActivityType] = Field(
        ..., description="Activity type at the origin of the trip to the airport"
    )
    """
    Activity type at the origin of the trip to the airport.
    """

    origin_activity_type_other: NoneOrNanString[str] = Field(
        ..., description="Activity type at the origin of the trip to the airport"
    )
    """
    Activity type at the origin of the trip to the airport.

    """
    origin_name: NoneOrNanString[str] = Field(
        ..., description="Place name of the origin of the trip to the airport"
    )
    """
    Place name of the origin of the trip to the airport.
    """

    origin_place_name: NoneOrNanString[str] = Field(
        ..., description="Postal City of the origin address for the trip to the airport"
    )
    """
    Postal City of the origin address for the trip to the airport.
    """

    origin_state: NoneOrNanString[str] = Field(
        ..., description="State of the origin address for the trip to the airport"
    )
    """
    State of the origin address for the trip to the airport.
    """

    origin_zip: NoneOrNanString[Union[str, int]] = Field(
        ..., description="ZIP code of the origin address for the trip to the airport"
    )
    """
    ZIP code of the origin address for the trip to the airport.
    """

    origin_latitude: NoneOrNanString[Latitude] = Field(
        ..., description="Latitude coordinate of the origin address for the trip to the airport"
    )
    """
    Latitude coordinate of the origin address for the trip to the airport.
    """

    origin_longitude: NoneOrNanString[Longitude] = Field(
        ..., description="Longitude coordinate of the origin address for the trip to the airport"
    )
    """
    Longitude coordinate of the origin address for the trip to the airport.
    """

    origin_municipal_zone: NoneOrNanString[str] = Field(
        ..., description="Municipal zone of the origin address for the trip to the airport"
    )
    """
    Municipal zone of the origin address for the trip to the airport
    """

    origin_pmsa: NoneOrNanString[e.PMSA] = Field(
        ..., description="Pseudo MSA of the origin address for the trip to the airport"
    )
    """
    Pseudo MSA of the origin address for the trip to the airport
    """
    
    destination_activity_type: NoneOrNanString[e.ActivityType] = Field(
        ...,
        description="Activity type at the destination of the trip from the airport",
    )
    """
    Activity type at the destination of the trip from the airport.
    """

    destination_activity_type_other: NoneOrNanString[str] = Field(
        ...,
        description="Activity type (other) at the destination of the trip from the airport",
    )
    """
    Activity type (other) at the destination of the trip from the airport.
    """

    @computed_field(
        return_type = e.ActivityType,
        description="Activity type prior to traveling to the airport (for inbound) or activity traveling to do next (for outbound).",
    )
    @property
    def non_airport_activity_type(cls):
        """
        Activity type prior to traveling to the airport (for inbound) or activity traveling to do next (for outbound).
        """
        if cls.inbound_or_outbound == e.InboundOutbound.INBOUND_TO_AIRPORT:
            return cls.origin_activity_type
        return cls.destination_activity_type

    destination_name: NoneOrNanString[str] = Field(
    ..., description="Place name of the destination from the airport"
    )
    """
    Place name of the destination from the airport.
    """

    destination_place_name: NoneOrNanString[str] = Field(
        ..., description="Postal City of the destination address from the airport"
    )
    """
    Postal City of the destination address from the airport.
    """

    destination_state: NoneOrNanString[str] = Field(
        ..., description="State of the destination address from the airport"
    )
    """
    State of the destination address from the airport.
    """

    destination_zip: NoneOrNanString[Union[str, int]] = Field(
        ..., description="ZIP code of the destination address from the airport"
    )
    """
    ZIP code of the destination address from the airport.
    """

    destination_latitude: NoneOrNanString[Latitude] = Field(
        ..., description="Latitude coordinate of the destination address from the airport"
    )
    """
    Latitude coordinate of the destination address from the airport.
    """

    destination_longitude: NoneOrNanString[Longitude] = Field(
        ..., description="Longitude coordinate of the destination address from the airport"
    )
    """
    Longitude coordinate of the destination address from the airport.
    """

    destination_municipal_zone: NoneOrNanString[str] = Field(
        ..., description="Municipal zone of the destination address for the trip to the airport"
    )
    """
    Municipal zone of the destination address for the trip to the airport
    """

    destination_pmsa: NoneOrNanString[e.PMSA] = Field(
        ..., description="Pseudo MSA of the destination address for the trip to the airport"
    )
    """
    Pseudo MSA of the origin destination for the trip to the airport
    """

    main_transit_mode: NoneOrNanString[e.TravelMode] = Field(
        ..., description = "Main Transit mode to/from airport"
    )
    """
    Main Transit mode to/from airport.
    """

    main_mode: NoneOrNanString[e.TravelMode] = Field(
        ..., description = "Main Mode to/from airport"
    )
    """
    Main Mode to/from airport.
    """

    main_mode_other: NoneOrNanString[str] = Field(
        ..., description = "Name of the other Main Mode to/from airport"
    )
    """
    Name of the other Main Mode to/from airport.
    """
    
    main_mode_grouped: NoneOrNanString[e.TravelModeGrouped] = Field(
        ..., description = "Grouped Main Mode to/from airport")
    """
    Grouped Main Mode to/from airport
    """

    shared_van_other: NoneOrNanString[str] = Field(
        ..., description = "Name of the other shared van service used by respondent"
    )
    """
    Name of the other shared van service used by respondent.
    """

    number_transit_vehicles_to_airport: NoneOrNanString[e.NumTransfers] = Field(
        ..., description = "Number of transit transfers for the inbound trip to the airport"
    )
    """
    Number of transit transfers for the inbound trip to the airport
    """

    to_airport_transit_route_1: NoneOrNanString[str] = Field(
        ..., description="Name of the First Transit Route to the airport"
    )
    """
    Name of the First Transit Route to the airport
    """

    to_airport_transit_route_1_other: NoneOrNanString[str] = Field(
        ..., description="Other First Transit Route to the airport"
    )
    """
    Other First Transit Route to the airport
    """

    to_airport_transit_route_2: NoneOrNanString[str] = Field(
        ..., description="Name of the Second Transit Route to the airport"
    )
    """
    Name of the Second Transit Route to the airport
    """

    to_airport_transit_route_2_other: NoneOrNanString[str] = Field(
        ..., description="Other Second Transit Route to the airport"
    )
    """
    Other Second Transit Route to the airport
    """

    to_airport_transit_route_3: NoneOrNanString[str] = Field(
        ..., description="Name of the Third Transit Route to the airport"
    )
    """
    Name of the Third Transit Route to the airport
    """

    to_airport_transit_route_3_other: NoneOrNanString[str] = Field(
        ..., description="Other Third Transit Route to the airport"
    )
    """
    Other Third Transit Route to the airport
    """

    to_airport_transit_route_4: NoneOrNanString[str] = Field(
        ..., description="Name of the Fourth Transit Route to the airport"
    )
    """
    Name of the Fourth Transit Route to the airport
    """

    to_airport_transit_route_4_other: NoneOrNanString[str] = Field(
        ..., description="Other Fourth Transit Route to the airport"
    )
    """
    Other Fourth Transit Route to the airport
    """

    transit_routes_list: NoneOrNanString[str] = Field(
        ..., description = "List of transit routes used by the respondent (comma separated)"
    )
    """
    List of transit routes used by the respondent (comma separated)
    """

    num_transit_transfers: NoneOrNanString[int] = Field(
        ..., description = "Number of transit transfers made by the respondent"
    )
    """
    Number of transit transfers made by the respondent.
    """
    
    access_mode: NoneOrNanString[e.TravelMode] = Field(
        ..., description = "Access mode to first transit vehicle for inbound trip to the airport"
    )
    """
    Access mode to first transit vehicle for inbound trip to the airport.
    """

    access_mode_other: NoneOrNanString[str] = Field(
        ..., description = "Other Access mode to first transit vehicle for inbound trip to the airport"
    )
    """
    Other Access mode to first transit vehicle for inbound trip to the airport.
    """

    access_mode_grouped: NoneOrNanString[e.TravelModeGrouped] = Field(
        ..., description = "Grouped Access mode to first transit vehicle for inbound trip to the airport"
    )
    """
    Grouped Access mode to first transit vehicle for inbound trip to the airport.
    """

    taxi_fhv_fare: NoneOrNanString[Union[str,float]] = Field(
        ..., description = "Taxi or for-hire vehicle fare"
    )
    """
    Taxi or for-hire vehicle fare.
    """

    taxi_fhv_wait: NoneOrNanString[Union[str,float]] = Field(
        ..., description = "Wait time for taxi or for-hire vehicle"
    )
    """
    Wait time for taxi or for-hire vehicle.
    """

    parking_location: NoneOrNanString[e.ParkingLocation] = Field(
        ..., description = "Name of respondent's parking location. "
    )
    """
    Name of respondent's parking location. 
    """

    parking_location_other: NoneOrNanString[str] = Field(
        ..., description = "Name of respondent's (other) parking location. "
    )
    """
    Name of respondent's (other) parking location. 
    """

    parking_cost: NoneOrNanString[Union[str,float]] = Field(
        ..., description = "Amount respondent paid to park"
    )
    """
    Amount respondent paid to park.
    """

    @computed_field(
        return_type = float,
        description = "Numeric value of the taxi fare",
    )
    @property
    def taxi_fhv_fare_numeric(cls):
        """
        Numeric Value of Taxi Fare
        """
        if isinstance(cls.taxi_fhv_fare, str):
            numeric_value = re.findall(r"[-+]?\d*\.?\d+|\d+", cls.taxi_fhv_fare)
            return numeric_value[0] if numeric_value else None
        return cls.taxi_fhv_fare
        
    @computed_field(
        return_type = float,
        description = "Numeric value of the taxi Wait Time",
    )
    @property
    def taxi_fhv_wait_numeric(cls):
        """
        Numeric Value of Taxi Wait Time
        """
        if isinstance(cls.taxi_fhv_wait, str):
            numeric_value = re.findall(r"[-+]?\d*\.?\d+|\d+", cls.taxi_fhv_wait)
            return numeric_value[0] if numeric_value else None
        return cls.taxi_fhv_wait

    @computed_field(
        return_type = float,
        description = "Numeric value of parking cost",
    )
    @property
    def parking_cost_numeric(cls):
        """
        Numeric Value of parking cost
        """
        if isinstance(cls.parking_cost, str):
            numeric_value = re.findall(r"[-+]?\d*\.?\d+|\d+", cls.parking_cost)
            return numeric_value[0] if numeric_value else None
        return cls.parking_cost

    
    # @model_validator(mode="before")
    # def convert_datetime(cls, values):
    #     # List of fields to validate
    #     fields_to_check = ['taxi_fhv_fare', 'taxi_fhv_wait', 'parking_cost']
        
    #     for field in fields_to_check:
    #         value = values.get(field)
    #         if isinstance(value, datetime):
    #             # Option 1: Convert datetime to float (timestamp)
    #             # values[field] = value.timestamp()

    #             # Option 2: Convert datetime to a formatted string
    #             values[field] = value.strftime('%Y-%m-%d %H:%M:%S')
    #             values['valid_record'] = False
    #             values['validation_severity'] = "Low"
    #             values['validation_error'] = field + f"{field} is datetime"

    #     return values


    parking_cost_frequency: NoneOrNan[e.ParkingCostFrequency] = Field(
        ..., description = "Frequency of reported parking cost (e.g., one-time, per hour, per day, per month)"
    )
    """
    Frequency of reported parking cost (e.g., one-time, per hour, per day, per month)
    """

    parking_cost_frequency_other: NoneOrNanString[Union[str, int]] = Field(
        ..., description = "Other frequency of reported parking cost"
    )
    """
    Other frequency of reported parking cost
    """

    reimbursement: NoneOrNan[e.ParkingReimbursement] = Field(
        ..., description = "Whether or not ground access cost will be reimbursed by employer or other non-household member"
    )
    """
    Whether or not ground access cost will be reimbursed by employer or other non-household member.
    """

    number_transit_vehicles_from_airport: NoneOrNanString[e.NumTransfers] = Field(
        ..., description = "Number of transit transfers for the inbound trip"
    )
    """
    Number of transit transfers for the inbound trip.
    """

    from_airport_transit_route_1: NoneOrNanString[str] = Field(
        ..., description="Name of the First Transit Route from the airport"
    )
    """
    Name of the First Transit Route from the airport
    """

    from_airport_transit_route_1_other: NoneOrNanString[str] = Field(
        ..., description="Other First Transit Route from the airport"
    )
    """
    Other First Transit Route from the airport
    """

    from_airport_transit_route_2: NoneOrNanString[str] = Field(
        ..., description="Name of the Second Transit Route from the airport"
    )
    """
    Name of the Second Transit Route from the airport
    """

    from_airport_transit_route_2_other: NoneOrNanString[str] = Field(
        ..., description="Other Second Transit Route from the airport"
    )
    """
    Other Second Transit Route from the airport
    """

    from_airport_transit_route_3: NoneOrNanString[str] = Field(
        ..., description="Name of the Third Transit Route from the airport"
    )
    """
    Name of the Third Transit Route from the airport
    """

    from_airport_transit_route_3_other: NoneOrNanString[str] = Field(
        ..., description="Other Third Transit Route from the airport"
    )
    """
    Other Third Transit Route from the airport
    """

    from_airport_transit_route_4: NoneOrNanString[str] = Field(
        ..., description="Name of the Fourth Transit Route from the airport"
    )
    """
    Name of the Fourth Transit Route from the airport
    """

    from_airport_transit_route_4_other: NoneOrNanString[str] = Field(
        ..., description="Other Fourth Transit Route from the airport"
    )
    """
    Other Fourth Transit Route from the airport
    """

    egress_mode: NoneOrNanString[e.TravelMode] = Field(
        ..., description = "Egress mode from last transit vehicle for outbound trip"
    )
    """
    Egress mode from last transit vehicle for outbound trip.
    """

    egress_mode_other: NoneOrNanString[str] = Field(
        ..., description = "Other Egress mode from last transit vehicle for outbound trip"
    )
    """
    Other Egress mode from last transit vehicle for outbound trip.
    """

    egress_mode_grouped: NoneOrNanString[e.TravelModeGrouped] = Field(
        ..., description = "Grouped Egress mode from last transit vehicle for outbound trip"
    )
    """
    Grouped Egress mode from last transit vehicle for outbound trip.
    """

    transit_boarding_stop_name: NoneOrNanString[str] = Field(
        ..., description = "Name of the stop where respondent boarded the main transit mode"
    )
    """
    Name of the stop where respondent boarded the main transit mode
    """

    transit_boarding_latitude: NoneOrNanString[Latitude] = Field(
        ..., description = "Latitude of the stop where respondent boarded the main transit mode"
    )
    """
    Latitude of the stop where respondent boarded the main transit mode
    """

    transit_boarding_longitude: NoneOrNanString[Longitude] = Field(
        ..., description = "Longitude of the stop where respondent boarded the main transit mode"
    )
    """
    Longitude of the stop where respondent boarded the main transit mode
    """

    transit_alighting_stop_name: NoneOrNanString[str] = Field(
        ..., description = "Name of the stop where respondent got off the main transit mode"
    )
    """
    Name of the stop where respondent got off the main transit mode
    """

    transit_alighting_latitude: NoneOrNanString[Latitude] = Field(
        ..., description = "Latitude of the stop where respondent got off the main transit mode"
    )
    """
    Latitude of the stop where respondent got off the main transit mode
    """

    transit_alighting_longitude: NoneOrNanString[Longitude] = Field(
        ..., description = "Longitude of the stop where respondent got off the main transit mode"
    )
    """
    Longitude of the stop where respondent boarded the main transit mode
    """

    
    @model_validator(mode="after")
    def validate_record(cls, values):
        
        errors, severity_levels, num_errors = skip_logic_validator.validate("Trip", values.dict())
        # Update validation fields
        #values.valid_record = len(errors) == 0
        values.validation_error = errors
        values.validation_severity = cls.determine_severity(severity_levels)
        values.validation_num_errors = num_errors
        
        return values
    
    @staticmethod
    def determine_severity(severity_levels):
        if severity_levels["Critical"] > 0:
            return "Critical"
        elif severity_levels["Non-Critical"] > 0:
            return "Non-Critical"
        return "None"
    pass 

class Respondent(PydanticModel):
    """
    Data model for a survey respondent. It includes attributes common to air passengers and employees.
    """

    is_completed: bool = Field(
        ..., description = "True if the record is complete"
    )
    """
    True if the record is complete
    """

    is_self_administered: bool = Field(
        default = False, description = "True if the survey was self-administered by the respondent")
    """
    True if the survey was self-administered by the respondent.
    """
    
    respondentid: Union[int,str] = Field(
        ..., description="Unique identifier for the respondent")
    """
    Unique identifier for the respondent.
    """

    is_pilot: bool = Field(
        ..., description = "True if the record was collected during the pilot survey"
    )
    """
    True if the record was collected during the pilot survey
    """

    record_type_synthetic: bool =  Field(
        ..., description = "True if the record is synthetically generated"
    )
    """
    True if the record is synthetically generated
    """


    date_completed: NoneOrNanString[datetime] = Field(
        ..., description = "Date when respondent completed the survey"
    )
    """
    Date when respondent completed the survey
    """

    time_completed: NoneOrNanString[time] = Field(
        ..., description = "Time when respondent completed the survey"
    )
    """
    Time when respondent completed the survey
    """


    initial_etc_check: NoneOrNanString[bool] = Field(
        ..., description = "True if the record passed ETC's initial check"
    )

    """
    True if the record is to be used for submittal
    """


    @computed_field(
        return_type = bool,
        description = "True if the record was captured during Thanksgiving Week",
    )
    @property
    def thanksgiving_week_flag(cls):
        """
        True if the record was captured during Thanksgiving Week
        """

        thanksgiving_start = pd.Timestamp('2024-11-25')  # Monday
        if cls.date_completed is None or pd.isna(cls.date_completed):
            return False  # or handle as needed
        if thanksgiving_start <= cls.date_completed:
            return True
        else:
            return False
        


    weight: float = Field(
        ..., description = 'Default expansion Factor of the observation, used in expansion script downstream'
    )
    """
    Default expansion Factor of the observation, used in the expansion script downstream
    """

    weight_departing_and_arriving: float = Field(
        ..., description = 'Weights corresponding to arriving and departing passengers expansion (also includes synthetic records)'
    )
    """
    Weights corresponding to arriving and departing expansion (also includes synthetic records)
    """

    weight_departing_only: float = Field(
        ..., description = 'Weights corresponding to only departing passengers expansion (no synthetic/arriving passengers)'
    )
    """
    Weights corresponding to only departing passengers expansion (no synthetic/arriving passengers)
    """

    weight_non_sas_departing_only: float = Field(
        ..., description = 'Weights corresponding to only departing and intercept survey passengers expansion (no self-administered survey responses, or synthetic records)'
    )
    """
    Weights corresponding to only departing and intercept survey passengers expansion (no self-administered survey responses or synthetic records)
    """


    weight_departing_only_with_time_of_day: float = Field(
        ..., description = 'Weights corresponding to only departing passengers expansion including time-of-day controls (no synthetic/arriving passengers)'
    )
    """
    Weights corresponding to only departing passengers expansion including time-of-day controls (no synthetic/arriving passengers)
    """

    
    interview_location: NoneOrNan[e.InterviewLocation] = Field(
        ..., description = "Location where respondent was intercepted")
    """
    Location where respondent was intercepted.
    """

    interview_location_other: NoneOrNanString[str] = Field(
        ..., description = "Other Location where respondent was intercepted")
    """
    Other Location where respondent was intercepted
    """

    marketsegment: NoneOrNan[e.Type] = Field(
        ..., description="Type of respondent, either passenger, employee, or other"
    )
    """
    Type of respondent, either passenger, employee, or other.
    """

    resident_visitor_purpose: NoneOrNanString[e.ResidentVisitorPurpose] = Field(
        ..., description = "Determines the resident/visitor classification based on the home airport status and flight purpose"
    )
    """
    Determines the resident/visitor classification based on the home airport status and flight purpose
    """

    is_qualified_age: NoneOrNanString[bool] = Field(
        ...,
        description="Whether the respondent is of a qualified age to participate in the survey",
    )
    """
    Whether the respondent is of a qualified age to participate in the survey.
    """

    resident_visitor: NoneOrNan[e.ResidentVisitor] = Field(
        ...,
        description="Where the respondent resides in the airport service area most of the year",
    )
    """
    Where the respondent resides in the airport service area most of the year.
    """

    home_location_place_name: NoneOrNanString[str] =  Field(
        ..., description = "Postal City of the home location of the respondent"
    )
    """
    Postal City of the home location of the respondent
    """

    home_location_state: NoneOrNanString[str] =  Field(
        ..., description = "State of the home location of the respondent"
    )
    """
    State of the home location of the respondent
    """

    home_location_zip: NoneOrNanString[Union[str,int]] =  Field(
        ..., description = "ZIP of the home location of the respondent"
    )
    """
    ZIP of the home location of the respondent
    """

    home_location_latitude: NoneOrNanString[Latitude] =  Field(
        ..., description = "Latitude of the home location of the respondent"
    )
    """
    Latitude of the home location of the respondent
    """

    home_location_longitude: NoneOrNanString[Longitude]=   Field(
        ..., description = "Longitude of the home location of the respondent"
    )
    """
    Longitude of the home location of the respondent
    """

    home_location_municipal_zone: NoneOrNanString[str] = Field(
        ..., description="Municipal zone of home address of the respondent"
    )
    """
    Municipal zone of home address of the Resident
    """

    home_location_pmsa: NoneOrNanString[e.PMSA] = Field(
        ..., description="Pseudo MSA of home address of the Resident"
    )
    """
    Pseudo MSA of home address of the Resident
    """

    number_of_travel_companions: NoneOrNanString[e.PartySize] = Field(
        ..., description = "Number of people flying with the respondent (count excludes the respondent)"
    )
    """
    Number of people flying with the respondent (count excludes the respondent)
    """

    party_size_flight: NoneOrNan[int] = Field(
        ..., description = "Size of the travel party"
    )
    """
    Size of the travel party
    """
 #Add new here
    # home_location_address: NoneOrNanString[str] =  Field(
    #     ..., description = "Street Address of the home location of the respondent"
    # )
    # """
    # Street Address of the home location of the respondent
    # """

    age: NoneOrNan[e.Age] = Field(..., description="Age category of the respondent")
    """
    Age category of the respondent.
    """

    gender: NoneOrNan[e.Gender] = Field(..., description="Gender of the respondent")
    """
    Gender of the respondent.
    """

    gender_other: NoneOrNanString[str] = Field(
        ..., description = "Gender of the respondent (not listed)"
    )
    """
    Gender of the respondent (not listed)
    """

    race_aian: NoneOrNanString[bool] = Field(
        ...,
        description="Does the respondent identify as American Indian or Alaska Native?",
    )
    """
    Does the respondent identify as American Indian or Alaska Native?
    """

    race_asian:  NoneOrNanString[bool] = Field(..., description="Does the respondent identify as Asian?")
    """
    Does the respondent identify as Asian?
    """

    race_black:  NoneOrNanString[bool] = Field(
        ..., description="Does the respondent identify as Black or African American?"
    )
    """
    Does the respondent identify as Black or African American?
    """

    race_hispanic:  NoneOrNanString[bool] = Field(
        ..., description="Does the respondent identify as Hispanic or Latino?"
    )
    """
    Does the respondent identify as Hispanic or Latino?
    """

    race_middle_eastern:  NoneOrNanString[bool] = Field(
        ..., description="Does the respondent identify as Middle Eastern?"
    )
    """
    Does the respondent identify as Middle Eastern?
    """

    race_hp:  NoneOrNanString[bool] = Field(
        ...,
        description="Does the respondent identify as Native Hawaiian or Other Pacific Islander?",
    )
    """
    Does the respondent identify as Native Hawaiian or Other Pacific Islander?
    """

    race_white:  NoneOrNanString[bool] = Field(..., description="Does the respondent identify as White?")
    """
    Does the respondent identify as White?
    """

    race_unknown:  NoneOrNanString[bool] = Field(
        ..., description="Does the respondent identify as an unknown"
    )
    """
    Does the respondent identify as an unknown race/ethnicity?
    """

    race_other: NoneOrNanString[str] = Field(
        ...,
        description="If the respondent enters a race/ethnicicy not listed above, this field will be populated",
    )
    """
    If the respondent enters a race/ethnicity not listed above, this field will be populated. 
    """

    race_list: NoneOrNanString[str] = Field(
        ...,
        description="List of Races the respondent identifies as (comma separated)",
    )
    """
    List of Races the respondent identifies as (comma separated)
    """

    number_persons_in_household: NoneOrNan[e.HouseholdSize] = Field(
        ..., description="Number of persons in the respondent's household"
    )
    """
    Number of persons in the respondent's household.
    """

    number_vehicles: NoneOrNan[e.HouseholdVehicles] = Field(
        ..., description="Number of vehicles in the respondent's household"
    )
    """
    Number of vehicles in the respondent's household.
    """

    household_income: NoneOrNan[e.HouseholdIncome] = Field(
        ..., description="Income range of the respondent's household"
    )
    """
    Income range of the respondent's household.
    """

    is_income_below_poverty: NoneOrNanString[e.YesNoType] = Field(
        ..., description="Is the respondent's household income below poverty?",
    )
    """
    Is the respondent's household income below poverty?
    """

    number_workers: NoneOrNan[e.HouseholdWorkers] = Field(
        ..., description="Number of workers in the respondent's household"
    )
    """
    Number of workers in the respondent's household.
    """

    sp_invitation: NoneOrNanString[e.YesNoType] = Field(
        ..., description = "Whether the respondent chose to participate in the SP Survey"
    )

    """
    Whether the respondent chose to participate in the SP Survey
    """

    stay_informed: NoneOrNanString[e.YesNoType] = Field(
        ..., description = "Whether the respondent chose to Stay Informed about the project"
    )

    """
    Whether the respondent chose to Stay Informed about the project
    """

    survey_language: NoneOrNanString[e.SurveyLanguage] = Field(
        ..., description = "Language of the Survey"
    )
    """
    Language of the Survey
    """

    survey_language_other: NoneOrNanString[str] =  Field(
        ..., description = "Other (not listed) language of the survey"
    )
    """
    Other (not listed) language of the survey
    """
    ##Add SP Fields:

    sp_feature_short_wait: NoneOrNan[e.SPImportance] = Field(
        ..., description="Level of importance assigned to having a short wait time (less than 10 minutes) for transit service."
    )
    """Level of importance assigned to having a short wait time (less than 10 minutes) for transit service."""

    sp_feature_seats_transit_stop: NoneOrNan[e.SPImportance] = Field(
        ..., description="Level of importance assigned to the availability of seats at the transit stop."
    )
    """Level of importance assigned to the availability of seats at the transit stop."""

    sp_feature_luggage_rack: NoneOrNan[e.SPImportance] = Field(
        ..., description="Level of importance assigned to having a luggage rack option on the transit service."
    )
    """Level of importance assigned to having a luggage rack option on the transit service."""

    sp_feature_seats_transit: NoneOrNan[e.SPImportance] = Field(
        ..., description="Level of importance assigned to having available seating on the transit vehicle."
    )
    """Level of importance assigned to having available seating on the transit vehicle."""

    sp_feature_no_delay: NoneOrNan[e.SPImportance] = Field(
        ..., description="Level of importance assigned to ensuring the transit service is not delayed by car traffic."
    )
    """Level of importance assigned to ensuring the transit service is not delayed by car traffic."""

    sp_feature_early_morning: NoneOrNan[e.SPImportance] = Field(
        ..., description="Level of importance assigned to the service starting early in the morning (before 5 AM)."
    )
    """Level of importance assigned to the service starting early in the morning (before 5 AM)."""

    sp_feature_late_night: NoneOrNan[e.SPImportance] = Field(
        ..., description="Level of importance assigned to the service operating past 10 PM."
    )
    """Level of importance assigned to the service operating past 10 PM."""

    sp_feature_weekend_frequency: NoneOrNan[e.SPImportance] = Field(
        ..., description="Level of importance assigned to frequent transit service availability on weekends."
    )
    """Level of importance assigned to frequent transit service availability on weekends."""

    sp_access_walk_time: NoneOrNan[e.SPWillingToWalkTime] = Field(
        ..., description="Maximum walking time (in minutes) the respondent is willing to take to access the transit station."
    )
    """Maximum walking time (in minutes) the respondent is willing to take to access the transit station."""

    sp_number_of_transfers: NoneOrNan[e.SPNumTransfers] = Field(
        ..., description="Number of transfers the respondent is willing to make to reach the airport."
    )
    """Number of transfers the respondent is willing to make to reach the airport."""

    sp_dropoff_escort: NoneOrNan[e.SPDropoffType] = Field(
        ..., description="Type of Person who dropped the respondent off at the airport."
    )
    """Type of Person who dropped the respondent off at the airport."""

    sp_dropoff_choice_no_transit_access: NoneOrNan[e.SPLikelihood] = Field(
        ..., description="Likelihood of being dropped off at the new transit station in areas without existing transit access."
    )
    """Likelihood of being dropped off at the new transit station in areas without existing transit access."""

    sp_dropoff_choice_transit_access: NoneOrNan[e.SPLikelihood] = Field(
        ..., description="Likelihood of being dropped off at a transit stop in areas with existing transit access."
    )
    """Likelihood of being dropped off at a transit stop in areas with existing transit access."""

    sp_taxi_choice_dropoff_station: NoneOrNan[e.SPLikelihood] = Field(
        ..., description="Likelihood of opting for drop-off at the new transit station when using a taxi."
    )
    """Likelihood of opting for drop-off at the new transit station when using a taxi."""

    sp_rental_choice_no_transit: NoneOrNan[e.SPLikelihood] = Field(
        ..., description="Likelihood of still renting a car if the new transit service were available."
    )
    """Likelihood of still renting a car if the new transit service were available."""

    sp_connection_to_santafe_depot: NoneOrNan[e.SPLikelihood] = Field(
        ..., description="Likelihood of using the new transit connection to the Santa Fe Depot train station."
    )
    """Likelihood of using the new transit connection to the Santa Fe Depot train station."""

    sp_connection_to_convention_center: NoneOrNan[e.SPLikelihood] = Field(
        ..., description="Likelihood of using the new transit connection to the San Diego Convention Center."
    )
    """Likelihood of using the new transit connection to the San Diego Convention Center."""

    sp_connection_to_old_town_center: NoneOrNan[e.SPLikelihood] = Field(
        ..., description="Likelihood of using the new transit connection to the Old Town Transit Center."
    )
    """Likelihood of using the new transit connection to the Old Town Transit Center."""

     # Missing fields related to other airports
    sp_other_airport_ease_of_planning: NoneOrNanString[bool] = Field(
        ..., description="True if the respondent found trip planning easy at another airport's transit service."
    )
    """True if the respondent found trip planning easy at another airport's transit service."""

    sp_other_airport_walking_distance: NoneOrNanString[bool] = Field(
        ..., description="True if the transit station at another airport was within a comfortable walking distance."
    )
    """True if the transit station at another airport was within a comfortable walking distance."""

    sp_other_airport_short_travel_time: NoneOrNanString[bool] = Field(
        ..., description="True if the respondent experienced a short total travel time at another airport."
    )
    """True if the respondent experienced a short total travel time at another airport."""

    sp_other_airport_no_delays: NoneOrNanString[bool] = Field(
        ..., description="True if the respondent experienced no delays using another airport's transit service."
    )
    """True if the respondent experienced no delays using another airport's transit service."""

    sp_other_airport_cost: NoneOrNanString[bool] = Field(
        ..., description="True if the cost of using transit at another airport was a positive factor."
    )
    """True if the cost of using transit at another airport was a positive factor."""

    sp_other_airport_frequency_of_service: NoneOrNanString[bool] = Field(   
        ..., description="True if the frequency of service at another airport was a positive factor."
    )
    """
    True if the frequency of service at another airport was a positive factor.
    """

    sp_other_airport_ease_of_boarding: NoneOrNanString[bool] = Field(
        ..., description="True if the respondent found boarding easy at another airport's transit service."
    )
    """True if the respondent found boarding easy at another airport's transit service."""

    sp_other_airport_comfort: NoneOrNanString[bool] = Field(
        ..., description="True if the respondent found the transit service at another airport comfortable."
    )
    """True if the respondent found the transit service at another airport comfortable."""

    sp_other_airport_safety: NoneOrNanString[bool] = Field(
        ..., description="True if the respondent felt safe using another airport's transit service."
    )
    """True if the respondent felt safe using another airport's transit service."""

    sp_other_airport_luggage_rack: NoneOrNanString[bool] = Field(
        ..., description="True if a luggage rack was available at another airport's transit service."
    )
    """True if a luggage rack was available at another airport's transit service."""

    sp_other_airport_enough_capacity: NoneOrNanString[bool] = Field(
        ..., description="True if there was sufficient passenger capacity at another airport."
    )
    """True if there was sufficient passenger capacity at another airport."""

    sp_other_airport_no_transfers: NoneOrNanString[bool] = Field(
        ..., description="True if no transfers were required at another airport's transit service."
    )
    """True if no transfers were required at another airport's transit service."""

    sp_other_airport_longer_operating_hours: NoneOrNanString[bool] = Field(
        ..., description="True if another airport's transit service had longer operating hours."
    )
    """True if another airport's transit service had longer operating hours."""

    sp_other_airport_enough_room_to_stand: NoneOrNanString[bool] = Field(
        ..., description="True if there was enough standing room at another airport's transit service."
    )
    """True if there was enough standing room at another airport's transit service."""

    sp_other_airport_enough_seats: NoneOrNanString[bool] = Field(
        ..., description="True if there were enough available seats at another airport's transit service."
    )
    """True if there were enough available seats at another airport's transit service."""

    sp_other_airport_other_specify: NoneOrNanString[bool] = Field(
        ..., description="True if the respondent liked something else about another airport’s transit service."
    )
    """True if the respondent liked something else about another airport’s transit service."""

    sp_other_airport_did_not_like: NoneOrNanString[bool] = Field(
        ..., description="True if the respondent did not like the transit service at another airport."
    )
    """True if the respondent did not like the transit service at another airport."""


    sp_other_airport_other: NoneOrNanString[str] = Field(
        ..., description="Additional comments provided by the respondent regarding another airport's transit service."
    )
    """Additional comments provided by the respondent regarding another airport's transit service."""

    sp_other_airport_list: NoneOrNanString[str] = Field(
        ..., description="List of factors at other airports due to which the respondent used transit service."
    )
    """
    List of factors at other airports due to which the respondent used transit service.
    """

    trip: Trip = Field(..., description="Details of the trip taken by the respondent")
    """
    Details of the trip taken by the respondent.
    """

    @model_validator(mode="after")
    def prefer_not_disclose_is_unique(cls, values):
        race_unknown = values.race_unknown
        race_aian = values.race_aian
        race_asian = values.race_asian
        race_black = values.race_black
        race_hispanic = values.race_hispanic
        race_middle_eastern = values.race_middle_eastern
        race_white = values.race_white
        if race_unknown and (
            race_aian
            or race_asian
            or race_black
            or race_hispanic
            or race_middle_eastern
            or race_white
        ):
            #values.race_unknown = False
            #values.valid_record= False
            values.validation_error = "Prefer Not to disclose cannot be combined with any other race"
            values.validation_severity = "Low"
        return values


class Employee(Respondent):
    """
    Data model for an employee respondent. It includes attributes specific to employees.
    """

    # shift_start_location: NoneOrNan[Coord] = Field(
    #     ..., description = "Longitude and Latitude of building where the employee starts their shift"
    # )
    # """
    # Longitude and Latitude of building where the employee starts their shift.
    # """
    
    trip_start_time: NoneOrNan[e.DepartTime] = Field(
        ..., description="Start time of the trip"
    )
    """
    Start time of the trip.
    """

    trip_arrival_time: NoneOrNan[e.DepartTime] = Field(
        ..., description="Arrival time of the trip"
    )
    """
    Arrival time of the trip.
    """

    shift_start_airport_building: NoneOrNanString[e.SanBuildings] = Field(
        ..., description = "Name of building where employee starts their shift"
    )
    """
    Name of building where employee starts their shift.
    """

    shift_start_airport_building_other: NoneOrNanString[str] = Field(
        ..., description = "Name of building (not listed) where employee starts their shift"
    )
    """
    Name of building (not listed) where employee starts their shift.
    """

    employer: NoneOrNanString[e.Employers] = Field(
        ..., description = "Name of respondent's employer"
    )
    """
    Name of  respondent's employer.
    """

    employer_other: NoneOrNanString[str] = Field(
        ..., description = "Name (not listed) of respondent's employer"
    )
    """
    Name (not listed) of respondent's employer.
    """

    occupation: NoneOrNanString[e.Occupations] = Field(
        ..., description = "Occupation of the employee"
    )
    """
    Occupation of the employee.
    """

    occupation_other: NoneOrNanString[str] = Field(
        ..., description = "Occupation (other, not listed) of the employee"
    )
    """
    Occupation (other, not listed) of the employee
    """

    occupation_detail: NoneOrNan[e.OccupationDetail] = Field(
        ..., description = "Occupation Details for the airport employee"
    )
    """
    Occupation Details for the airport employee
    """

    number_hours_worked: NoneOrNan[e.HoursWorked] = Field(
        ..., description = "Number of hours respondent worked in the past 7 days"
    )
    """
    Number of hours respondent worked in the past 7 days.
    """

    number_commute_days: NoneOrNan[e.CommuteDays] = Field(
        ..., description = "Number of days respondent commuted to the airport in the past 7 days"
    )
    """
    Number of days respondent commuted to the airport in the past 7 days.
    """

    shift_start_time: NoneOrNan[e.DepartTime] = Field(
        ..., description = "Time when the employee's shift starts"
    )
    """
    Time when the employee's shift starts.
    """

    shift_end_time: NoneOrNan[e.DepartTime] = Field(
        ..., description = "Time when the employee's shift ends"
    )
    """
    Time when the employee's shift ends.
    """
# Add New Here

    reverse_commute_mode: NoneOrNan[e.TravelMode] = Field(
        ..., description = "Reverse commute mode for the employee"
    )
    """
    Reverse commute mode for the employee
    """

    reverse_commute_mode_other: NoneOrNanString[str] = Field(
        ..., description = "Reverse commute mode for the employee (other, not listed)"
    )
    """
    Reverse commute mode for the employee (other, not listed)
    """

    reverse_commute_mode_grouped: NoneOrNanString[e.TravelModeGrouped] = Field(
        ..., description = "Grouped reverse commute mode for the employee"
    )
    """
    Grouped reverse commute mode for the employee
    """

    same_commute_mode: NoneOrNanString[e.YesNoType] = Field(
        ..., description = "True if the employee always used the same travel mode to commute in the last 30 days"
    )
    """
    True if the employee always used the same travel mode to commute in the last 30 days
    """

    same_commute_mode_other: NoneOrNanString[str] = Field(
        ..., description = "Other Response to employee's travel mode to commute in the last 30 days"
    )
    """
    Other Response to employee's travel mode to commute in the last 30 days
    """

    alt_commute_mode_taxi: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee used Taxi as a mode to commute to the airport in the past 30 days"
    )
    """
    True if the employee used Taxi as a mode to commute to the airport in the past 30 days.
    """
    
    alt_commute_mode_uber_lyft: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee used Uber or Lyft as a mode to commute to the airport in the past 30 days"
    )
    """
    True if the employee used Uber or Lyft as a mode to commute to the airport in the past 30 days.
    """
    
    alt_commute_mode_car_black: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee used a black car service as a mode to commute to the airport in the past 30 days"
    )
    """
    True if the employee used a black car service as a mode to commute to the airport in the past 30 days.
    """
    
    alt_commute_mode_picked_by_family_friend: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee was picked up by a family member or friend to commute to the airport in the past 30 days"
    )
    """
    True if the employee was picked up by a family member or friend to commute to the airport in the past 30 days.
    """
    
    alt_commute_mode_parked_vehicle_and_drive_alone: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee drove alone and parked their vehicle while commuting to the airport in the past 30 days"
    )
    """
    True if the employee drove alone and parked their vehicle while commuting to the airport in the past 30 days.
    """
    
    alt_commute_mode_parked_vehicle_and_drive_with_others: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee drove with others and parked their vehicle while commuting to the airport in the past 30 days"
    )
    """
    True if the employee drove with others and parked their vehicle while commuting to the airport in the past 30 days.
    """
    
    alt_commute_mode_parked_vehicle_and_ride_with_other_travelers: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee rode with other travelers and parked their vehicle while commuting to the airport in the past 30 days"
    )
    """
    True if the employee rode with other travelers and parked their vehicle while commuting to the airport in the past 30 days.
    """
    
    alt_commute_mode_mts_route_992: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee used MTS Route 992 to commute to the airport in the past 30 days"
    )
    """
    True if the employee used MTS Route 992 to commute to the airport in the past 30 days.
    """
    
    alt_commute_mode_airport_flyer_shuttle: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee used the Airport Flyer Shuttle to commute to the airport in the past 30 days"
    )
    """
    True if the employee used the Airport Flyer Shuttle to commute to the airport in the past 30 days.
    """
    
    alt_commute_mode_other_public_transit: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee used other public transit services to commute to the airport in the past 30 days"
    )
    """
    True if the employee used other public transit services to commute to the airport in the past 30 days.
    """
    
    alt_commute_mode_other_shared_van: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee used another type of shared van service to commute to the airport in the past 30 days"
    )
    """
    True if the employee used another type of shared van service to commute to the airport in the past 30 days.
    """
    
    alt_commute_mode_walk: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee walked as a mode to commute to the airport in the past 30 days"
    )
    """
    True if the employee walked as a mode to commute to the airport in the past 30 days.
    """
    
    alt_commute_mode_wheelchair: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee used a wheelchair to commute to the airport in the past 30 days"
    )
    """
    True if the employee used a wheelchair to commute to the airport in the past 30 days.
    """
    
    alt_commute_mode_bicycle_electric_bikeshare: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee used an electric bicycle through a bikeshare service to commute to the airport in the past 30 days"
    )
    """
    True if the employee used an electric bicycle through a bikeshare service to commute to the airport in the past 30 days.
    """
    
    alt_commute_mode_bicycle_non_electric_bikeshare: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee used a non-electric bicycle through a bikeshare service to commute to the airport in the past 30 days"
    )
    """
    True if the employee used a non-electric bicycle through a bikeshare service to commute to the airport in the past 30 days.
    """
    
    alt_commute_mode_bicycle_personal_electric_bicycle: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee used their personal electric bicycle to commute to the airport in the past 30 days"
    )
    """
    True if the employee used their personal electric bicycle to commute to the airport in the past 30 days.
    """
    
    alt_commute_mode_bicycle_personal_non_electric_bicycle: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee used their personal non-electric bicycle to commute to the airport in the past 30 days"
    )
    """
    True if the employee used their personal non-electric bicycle to commute to the airport in the past 30 days.
    """
    
    alt_commute_mode_e_scooter_shared: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee used a shared e-scooter to commute to the airport in the past 30 days"
    )
    """
    True if the employee used a shared e-scooter to commute to the airport in the past 30 days.
    """
    
    alt_commute_mode_e_scooter_personal: NoneOrNanString[bool] = Field(
        ..., description = "True if the employee used their personal e-scooter to commute to the airport in the past 30 days"
    )
    """
    True if the employee used their personal e-scooter to commute to the airport in the past 30 days.
    """

    alt_commute_mode_other: NoneOrNanString[str] = Field(
        ..., description = "Other mode used by the employee to commute to the airport in the past 30 days."
    )
    """
    Other mode used by the employee to commute to the airport in the past 30 days
    """

    alt_commute_mode_list: NoneOrNanString[str] = Field(
        ..., description = "List of modes used by the employee to commute to the airport in the past 30 days.")
    """
    List of modes used by the employee to commute to the airport in the past 30 days
    """


    commute_mode_decision: NoneOrNanString[e.ModeDecision] = Field(
        ..., description = "Factor affecting the Mode choice of the employee"
    )
    """
    Factor affecting the Mode choice of the employee
    """

    commute_mode_decision_other: NoneOrNanString[str] = Field(
        ..., description = "(Other) Factor affecting the Mode choice of the employee"
    )
    """
    (Other) Factor affecting the Mode choice of the employee
    """

    # past_commute_modes: List[NoneOrNan[e.TravelMode]] = Field(
    #     ..., description = "Modes used to commute to SDIA in the past 12 months"
    # )
    # """
    # Modes used to commute to SDIA in the past 12 months.
    # """

    # alternative_commute_modes: List[NoneOrNan[e.TravelMode]] = Field(
    #     ..., description = "Modes used to travel to SDIA in the past 30 days"
    # )
    # """
    # Modes used to travel to SDIA in the past 30 days.
    # """

    # commute_mode_decision: List[NoneOrNan[e.CommuteModeDecision]] = Field(
    #     ..., description = "Factors affecting mode choice, for respondents who do not always use the same mode"
    # )
    # """
    # Factors affecting mode choice, for respondents who do not always use the same mode.
    # """

    employee_parking: NoneOrNanString[bool] = Field(
        ..., description = "Whether the respondent has access to employee parking"
    )
    """
    Whether the respondent has access to employee parking.
    """

    # @model_validator(mode="after")
    # def validate_missing_fields(cls, values):
    #     null_fields = [field for field, value in values if value is None and 'other' not in field]
    #     critical_fields = []
    #     if null_fields:
    #         values.valid_record = False
    #         values.validation_error = f"Missing Fields: {', '.join(null_fields)}"
    #         values.validation_num_errors = len(null_fields)
    #         if len(null_fields)>3:
    #             values.validation_severity = "High"
    #         else:
    #             values.validation_severity = "Low"
    #         if any(field in critical_fields for field in null_fields):
    #             values.validation_severity = "Critical"
    #     return values
    
    @model_validator(mode="after")
    def validate_record(cls, values):
        # Validate using SkipLogicValidator
        errors, severity_levels, num_errors = skip_logic_validator.validate("Employee", values.dict())
        # Update validation fields
        #values.valid_record = len(errors) == 0
        values.validation_error = errors
        values.validation_severity = cls.determine_severity(severity_levels)
        values.validation_num_errors = num_errors
        
        return values
    
    @staticmethod
    def determine_severity(severity_levels):
        if severity_levels["Critical"] > 0:
            return "Critical"
        elif severity_levels["Non-Critical"] > 0:
            return "Non-Critical"
        return "None"

class AirPassenger(Respondent):
    """
    Data model for an air passenger respondent. It includes attributes specific to air passengers.
    """

    resident_visitor_general: NoneOrNan[e.ResidentVisitorGeneral] = Field(
        ...,
        description="Whether a resident or a visitor of the San deigo airport service area",
    )
    """
    Whether a resident or a visitor of the San deigo airport service area.
    """

    resident_visitor_followup: NoneOrNanString[e.ResidentVisitorFollowup] = Field(
        ...,
        description="If neither a resident or a visitor, whether the respondent is visiting San Diego",
    )
    """
    If neither a resident or a visitor, whether the respondent is visiting San Diego.
    """

    resident_visitor_arriving: NoneOrNanString[bool] = Field(
        ..., description = "True if respondent lives outside San Diego Region and is going home by ground transportation"
    )

    """
    True if respondent lives outside San Diego Region and is going home by ground transportation
    """
    
    passenger_segment: NoneOrNan[e.PassengerSegment] = Field(
        ..., description="Segment of the air passenger: (Resident/Visitor and Arriving/Departing)"
    )
    """
    Segment of the air passenger: (Resident/Visitor and Arriving/Departing)
    """

    qualified_visitor: NoneOrNan[bool] = Field( 
        ..., description = "True if the respondent is a qualified visitor")
    """
    True if the respondent is a qualified visitor.
    """

    is_sdia_home_airport: NoneOrNan[bool] = Field(
        ..., description = "True if the respondent's home airport is SDIA"
    )
    """
    True if the respondent's home airport is SDIA
    """

    country_of_residence: NoneOrNan[e.Country] = Field(
        ...,
        description="Country of residence for international vistors",
    )
    """
    Country of residence for international vistors.
    """

    state_of_residence: NoneOrNan[e.State] = Field(
        ...,
        description="State of residence for US and Mexico residents",
    )
    """
    State of residence for US and Mexico residents.
    """

    passenger_type: NoneOrNanString[e.PassengerType] = Field(
        ..., description = "Type of Passenger: Arriving, Departing or Connecting"
    )
    """
    Type of Passenger: Arriving, Departing or Connecting
    """

    previous_or_next_airport: NoneOrNanString[str] = Field(
        ..., description = "Where is the respondent flying from/flying to"
    )
    """
    Where is the respondent flying from/flying to.
    """


    # @model_validator(mode="before")
    # def validate_airport(cls, values):
    #     # List of fields to validate
    #     fields_to_check = ['previous_or_next_airport']
        
    #     for field in fields_to_check:
    #         value = values.get(field)
    #         if not isinstance(value, str):
    #             values[field] = str(value)
    #             values['valid_record'] = False
    #             values['validation_severity'] = "Low"
    #             values['validation_error'] = f"{field} is not string"

    #     return values

    airline: NoneOrNanString[e.Airline] = Field(
        ..., description = "Airline of the respondent's flight"
    )
    """
    Airline of the respondent's flight.
    """

    airline_other: NoneOrNanString[str] = Field(
        ..., description = "Other (not listed) airline of the respondent's flight"
    )
    """
    Other (not listed) airline of the respondent's flight.
    """

    flight_number: NoneOrNanString[Union[str, int]] = Field(
        ..., description = "Flight number of the respondent's flight"
    )
    """
    Flight number of the respondent's flight.
    """

    is_direct_flight: NoneOrNanString[bool] =  Field(
        ..., description = "True if the passenger did not use/is not using any connecting flights in their journey"
    )
    """
    True if the passenger did not use/is not using any connecting flights in their journey
    """

    @computed_field(
        return_type = e.Terminal,
        description = "Airport Terminal for Air Passenger",
    )
    @property
    def airport_terminal(cls):
        """
        Airport Terminal for Air Passenger
        """
        if cls.interview_location == e.InterviewLocation.TERMINAL_1:
            return e.Terminal.TERMINAL_1
        if cls.interview_location == e.InterviewLocation.TERMINAL_2:
            return e.Terminal.TERMINAL_2
        
        #Deriving using Airline if location is not a terminal
        if cls.airline in range(1,14):
            return e.Terminal.TERMINAL_2
        elif cls.airline in [14,15,16,17]:
            return e.Terminal.TERMINAL_1
        else:
            return e.Terminal.UNKNOWN

    flight_purpose: NoneOrNanString[e.FlightPurpose] = Field(
        ..., description = "Purpose of the respondent's flight"
    )
    """
    Purpose of the respondent's flight.
    """

    flight_purpose_other: NoneOrNanString[str] = Field(
        ..., description = "Other (not listed) purpose of the respondent's flight"
    )
    """
    Other (not listed) purpose of the respondent's flight
    """


    # @computed_field(
    #     return_type = e.ResidentVisitorPurpose,
    #     description = "Determines the resident/visitor classification based on the home airport status and flight purpose",
    # )
    # @property
    # def resident_visitor_purpose(cls):
    #     """
    #     Determines the resident/visitor classification based on the home airport status and flight purpose.
    #     """
    #     if cls.is_sdia_home_airport == True and cls.flight_purpose in {e.FlightPurpose.BUSINESS_WORK, e.FlightPurpose.COMBINATION_BUSINESS_LEISURE}:
    #         return e.ResidentVisitorPurpose.RESIDENT_BUSINESS
    #     elif cls.is_sdia_home_airport == False:
    #         return e.ResidentVisitorPurpose.RESIDENT_NON_BUSINESS
    #     elif cls.flight_purpose in {e.FlightPurpose.BUSINESS_WORK, e.FlightPurpose.COMBINATION_BUSINESS_LEISURE}:
    #         return e.ResidentVisitorPurpose.VISITOR_BUSINESS
    #     else:
    #         return e.ResidentVisitorPurpose.VISITOR_NON_BUSINESS


    checked_bags: NoneOrNan[e.CheckedBags] = Field(
        ..., description = "Number of checked bags"
    )
    """
    Number of checked bags.
    """

    carryon_bags: NoneOrNan[e.CarryOns] = Field(
        ..., description = "Number of carry-on bags"
    )
    """
    Number of carry-on bags.
    """

    number_of_nights: NoneOrNan[e.TravelDuration] = Field(
        ..., description = "Number of nights the respondent will be visiting/away"
    )
    """
    Number of nights the respondent will be visiting/away
    """

    party_size_ground_access_same: NoneOrNanString[bool] = Field(
        ..., description = "Whether flying party all traveled to airport together"
    )
    """
    Whether flying party all traveled to airport together
    """

    party_size_ground_access: NoneOrNan[int] = Field(
        ..., description = "Size of ground access travel party"
    )
    """
    Size of ground access travel party
    """

    party_includes_child_aged00to05: NoneOrNanString[bool] = Field(
        ..., description = "True if the traveling party includes a child aged zero to two"
    )
    """
    True if the traveling party includes a child aged zero to two.
    """

    party_includes_child_aged06to17: NoneOrNanString[bool] = Field(
        ..., description = "True if the traveling party includes a child aged three to nine"
    )
    """
    True if the traveling party includes a child aged three to nine.
    """

    party_includes_coworker: NoneOrNanString[bool] = Field(
        ..., description = "True if the traveling party includes a coworker"
    )
    """
    True if the traveling party includes a coworker.
    """

    party_includes_friend_relative:  NoneOrNanString[bool] = Field(
        ..., description = "True if the traveling party includes a friend or relative"
    )
    """
    True if the traveling party includes a friend or relative.
    """

    party_includes_mobility_impaired:  NoneOrNanString[bool] = Field(
        ..., description = "True if the traveling party includes a mobility impaired person"
    )
    """
    True if the traveling party includes a mobility impaired person
    """

    party_composition_list: NoneOrNanString[str] = Field(
        ..., description = "List of people in the traveling party"
    )
    """
    List of people in the traveling party
    """

#Add here
    sdia_flight_frequency: NoneOrNan[e.SanFlightFrequency] = Field(
        ..., description = "Respondent's number of flights from SDIA in the past 12 months"
    )
    """
    Respondent's number of flights from SDIA in the past 12 months.
    """

    access_mode_frequency: NoneOrNan[e.SanFlightFrequency] = Field(
        ..., description = "Number of times respondent used revealed access modes for other SDIA airport access trips in the past 12 months"
    )
    """
    Number of times respondent used revealed access modes for other SDIA airport access trips in the past 12 months.
    """

#Distribution of all modes:
    sdia_accessmode_split_taxi: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent used taxi as a mode for his trip to SDIA in the last 12 months")
    """
    True if the respondent used taxi as a mode for his trip to SDIA in the last 12 months
    """

    sdia_accessmode_split_uber_lyft: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent used Uber or Lyft as a mode for their trip to SDIA in the last 12 months")
    """
    True if the respondent used Uber or Lyft as a mode for their trip to SDIA in the last 12 months
    """
    
    sdia_accessmode_split_car_black: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent used a black car or luxury service for their trip to SDIA in the last 12 months")
    """
    True if the respondent used a black car or luxury service for their trip to SDIA in the last 12 months
    """
    
    sdia_accessmode_split_dropped_off_by_family_friend: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent was dropped off by a family member or friend for their trip to SDIA in the last 12 months")
    """
    True if the respondent was dropped off by a family member or friend for their trip to SDIA in the last 12 months
    """
    
    sdia_accessmode_split_drove_alone_and_parked: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent drove alone and parked at SDIA in the last 12 months")
    """
    True if the respondent drove alone and parked at SDIA in the last 12 months
    """
    
    sdia_accessmode_split_drove_with_others_and_parked: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent drove with others and parked at SDIA in the last 12 months")
    """
    True if the respondent drove with others and parked at SDIA in the last 12 months
    """
    
    sdia_accessmode_split_rode_with_other_travelers_and_parked: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent rode with other travelers and parked at SDIA in the last 12 months")
    """
    True if the respondent rode with other travelers and parked at SDIA in the last 12 months
    """
    
    sdia_accessmode_split_mts992: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent used MTS992 for their trip to SDIA in the last 12 months")
    """
    True if the respondent used MTS992 for their trip to SDIA in the last 12 months
    """
    
    sdia_accessmode_split_flyer_shuttle: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent used the Flyer Shuttle for their trip to SDIA in the last 12 months")
    """
    True if the respondent used the Flyer Shuttle for their trip to SDIA in the last 12 months
    """
    
    sdia_accessmode_split_other_public_transit: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent used another form of public transit for their trip to SDIA in the last 12 months")
    """
    True if the respondent used another form of public transit for their trip to SDIA in the last 12 months
    """
    
    sdia_accessmode_split_rental_car_dropped_off: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent used a rental car and was dropped off at SDIA in the last 12 months")
    """
    True if the respondent used a rental car and was dropped off at SDIA in the last 12 months
    """
    
    sdia_accessmode_split_rental_car_parked: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent parked a rental car at SDIA in the last 12 months")
    """
    True if the respondent parked a rental car at SDIA in the last 12 months
    """
    
    sdia_accessmode_split_chartered_tour_bus: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent used a chartered tour bus for their trip to SDIA in the last 12 months")
    """
    True if the respondent used a chartered tour bus for their trip to SDIA in the last 12 months
    """
    
    sdia_accessmode_split_hotel_shuttle_van: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent used a hotel shuttle van for their trip to SDIA in the last 12 months")
    """
    True if the respondent used a hotel shuttle van for their trip to SDIA in the last 12 months
    """
    
    sdia_accessmode_split_employee_shuttle: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent used an employee shuttle for their trip to SDIA in the last 12 months")
    """
    True if the respondent used an employee shuttle for their trip to SDIA in the last 12 months
    """
    
    sdia_accessmode_split_other_shared_van: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent used another type of shared van service for their trip to SDIA in the last 12 months")
    """
    True if the respondent used another type of shared van service for their trip to SDIA in the last 12 months
    """
    
    sdia_accessmode_split_walk: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent walked to SDIA in the last 12 months")
    """
    True if the respondent walked to SDIA in the last 12 months
    """
    
    sdia_accessmode_split_wheelchair: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent used a wheelchair for their trip to SDIA in the last 12 months")
    """
    True if the respondent used a wheelchair for their trip to SDIA in the last 12 months
    """
    
    sdia_accessmode_split_bicycle_electric_bikeshare: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent used an electric bikeshare for their trip to SDIA in the last 12 months")
    """
    True if the respondent used an electric bikeshare for their trip to SDIA in the last 12 months
    """
    
    sdia_accessmode_split_bicycle_non_electric_bikeshare: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent used a non-electric bikeshare for their trip to SDIA in the last 12 months")
    """
    True if the respondent used a non-electric bikeshare for their trip to SDIA in the last 12 months
    """
    
    sdia_accessmode_split_bicycle_personal_electric_bicycle: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent used a personal electric bicycle for their trip to SDIA in the last 12 months")
    """
    True if the respondent used a personal electric bicycle for their trip to SDIA in the last 12 months
    """
    
    sdia_accessmode_split_bicycle_personal_non_electric_bicycle: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent used a personal non-electric bicycle for their trip to SDIA in the last 12 months")
    """
    True if the respondent used a personal non-electric bicycle for their trip to SDIA in the last 12 months
    """
    
    sdia_accessmode_split_e_scooter_shared: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent used a shared electric scooter for their trip to SDIA in the last 12 months")
    """
    True if the respondent used a shared electric scooter for their trip to SDIA in the last 12 months
    """
    
    sdia_accessmode_split_e_scooter_personal: NoneOrNanString[bool] = Field(
        ..., description  = "True if the respondent used a personal electric scooter for their trip to SDIA in the last 12 months")
    """
    True if the respondent used a personal electric scooter for their trip to SDIA in the last 12 months
    """
    
    sdia_accessmode_split_other: NoneOrNanString[str] = Field(
        ..., description = "Other mode the respondent used for their trip to SDIA in the last 12 months"
    )
    """
    Other mode the respondent used for their trip to SDIA in the last 12 months.
    """

    sdia_accessmode_split_list: NoneOrNanString[str] = Field(
        ..., description = "List of modes used by the respondent for their trip to SDIA in the last 12 months"
    )
    """
    List of modes used by the respondent for their trip to SDIA in the last 12 months.
    """

    sdia_accessmode_decision: NoneOrNan[e.ModeDecision] = Field(
        ..., description = "Factor which affects mode choice, for respondents who do not always used the same mode"
    )
    """
    Factor which affects mode choice, for respondents who do not always used the same mode.
    """

    sdia_transit_awareness: NoneOrNanString[e.YesNoType] = Field(
        ..., description = "Whether respondent is aware that buses are serving SDIA"
    )
    """
    Whether respondent is aware that buses are serving SDIA
    """
#Reasons to not use transit
    reasons_no_transit_not_convenient: NoneOrNanString[bool] = Field(
        ..., description = "True if the respondent did not use transit because it is not convenient"
    )
    """
    True if the respondent did not use transit because it is not convenient.
    """

    reasons_no_transit_too_complicated: NoneOrNanString[bool] = Field(
        ..., description = "True if the respondent did not use transit because it too complicated"
    )
    """
    True if the respondent did not use transit because it is too complicated.
    """ 

    reasons_no_transit_dont_know_how: NoneOrNanString[bool] = Field(
        ..., description = "True if the respondent did not use transit because they don't know how"
    )
    """
    True if the respondent did not use transit because they don't know how.
    """

    reasons_no_transit_no_good_options: NoneOrNanString[bool] = Field(
        ..., description = "True if the respondent did not use transit because there are no good options"
    )
    """
    True if the respondent did not use transit because there are no good options
    """

    reasons_no_transit_not_flexible: NoneOrNanString[bool] = Field(
        ..., description = "True if the respondent did not use transit because it is not flexible"
    )
    """
    True if the respondent did not use transit because it is not flexible.
    """

    reasons_no_transit_not_reliable: NoneOrNanString[bool] = Field(
        ..., description = "True if the respondent did not use transit because it is not reliable"
    )
    """
    True if the respondent did not use transit because it is not reliable.
    """

    reasons_no_transit_not_safe: NoneOrNanString[bool] = Field(
        ..., description = "True if the respondent did not use transit because it is not safe"
    )
    """
    True if the respondent did not use transit because it is not safe.
    """

    reasons_no_transit_ride_too_long: NoneOrNanString[bool] = Field(
        ..., description = "True if the respondent did not use transit because it takes too long"
    )
    """
    True if the respondent did not use transit because it takes too long
    """

    reasons_no_transit_wait_too_long: NoneOrNanString[bool] = Field(
        ..., description = "True if the respondent did not use transit because the wait time is too long"
    )
    """
    True if the respondent did not use transit because the wait time is too long
    """

    reasons_no_transit_does_not_run_when_needed: NoneOrNanString[bool] = Field(
        ..., description = "True if the respondent did not use transit because of it's schedule"
    )
    """
    True if the respondent did not use transit because of it's schedule
    """

    reasons_no_transit_too_many_transfers: NoneOrNanString[bool] = Field(
        ..., description = "True if the respondent did not use transit because it requries too many transfers"
    )
    """
    True if the respondent did not use transit because it requires too many transfers
    """

    reasons_no_transit_stop_too_far: NoneOrNanString[bool] = Field(
        ..., description = "True if the respondent did not use transit because the stop is too far"
    )
    """
    True if the respondent did not use transit because the stop is too far
    """

    reasons_no_transit_not_economical: NoneOrNanString[bool] = Field(
        ..., description = "True if the respondent did not use transit because it is not economical"
    )
    """
    True if the respondent did not use transit because it is not economical
    """

    reasons_no_transit_dislike_crowded_trains_buses: NoneOrNanString[bool] = Field(
        ..., description = "True if the respondent did not use transit because they don't like crowded trains and buses"
    )
    """
    True if the respondent did not use transit because they don't like crowded trains and buses.
    """

    reasons_no_transit_too_much_walking_stairs: NoneOrNanString[bool] = Field(
        ..., description = "True if the respondent did not use transit because it involves too much walking and/or stairs"
    )
    """
    True if the respondent did not use transit because it too much walking and/or stairs
    """

    reasons_no_transit_dislike_public_transport: NoneOrNanString[bool] = Field(
        ..., description = "True if the respondent did not use transit because they don't like public transport"
    )
    """
    True if the respondent did not use transit because they don't like public transport
    """

    reasons_no_transit_dislike_public_transport_with_luggage: NoneOrNanString[bool] = Field(
        ..., description = "True if the respondent did not use transit because they don't like public transport with luggage"
    )
    """
    True if the respondent did not use transit because they don't like public transport with luggage
    """

    reasons_no_transit_prefer_other_mode: NoneOrNanString[bool] = Field(
        ..., description = "True if the respondent did not use transit because they prefer other modes(s)"
    )
    """
    True if the respondent did not use transit because they prefer other mode(s)
    """

    reasons_no_transit_other: NoneOrNanString[str] = Field(
        ..., description = "Other reason why the respondent did not use transit"
    )
    """
    Other reason why the respondent did not use transit.
    """ 
    
    reasons_no_transit_list: NoneOrNanString[str] = Field(
        ..., description = "List of reasons why the respondent did not use transit"
    )
    """
    List of reasons why the respondent did not use transit.
    """

    non_sdia_flight_frequency: NoneOrNan[e.OtherFlightAndTransitUseFrequency] = Field(
        ..., description = "Respondent's number of flights from airport other than SDIA in the past 12 months"
    )
    """
    Respondent's number of flights from airport other than SDIA in the past 12 months.
    """

    other_airport_accessmode: NoneOrNanString[e.TravelMode] =  Field(
        ..., description = "Travel mode used to access other airports"
    )
    """
    Travel mode used to access other airports
    """

    other_airport_accessmode_grouped: NoneOrNanString[e.TravelModeGrouped] =  Field(
        ..., description = "Grouped Travel mode used to access other airports"
    )
    """
    Grouped Travel mode used to access other airports
    """

    airport_access_transit_use_elsewhere: NoneOrNanString[e.OtherFlightAndTransitUseFrequency] = Field(
        ..., description = "Frequency of Transit use by respondent to access other airports"
    )
    """
    Frequency of Transit use by respondent to access other airports.
    """

    airportaccesstransitname: NoneOrNanString[str] = Field(
        ..., description = "Name of other airport accessed by transit"
    )
    """
    Name of other airport accessed by transit.
    """
    
    pass 


class ArrivingAirPassenger(AirPassenger):
    """
    Data model for an arriving air passenger. It includes attributes specific to arriving air passengers.
    """

    @computed_field(
        return_type = str,
        description = "Previous flight origin for an arriving passenger",
    )
    @property
    def previous_flight_origin(cls):
        """
        Previous flight origin for an arriving passenger
        """
        if cls.passenger_type == e.PassengerType.ARRIVING:
            return cls.previous_or_next_airport
    
    @computed_field(
        return_type = bool,
        description = "True if the previous flight origin was original and not a layover",
    )
    @property
    def is_original_origin(cls):
        """
        True if the previous flight origin was original and not a layover
        """
        return cls.is_direct_flight
    
    flight_arrival_time: NoneOrNan[e.DepartTime] = Field(
        ..., description = "Time of flight arrival"
    )
    """
    Time of flight arrival.
    """

    original_flight_origin: NoneOrNanString[str] = Field(
        ..., description = "Original origin for arriving passengers"
    )
    """
    Original origin for arriving passengers.
    """

class DepartingAirPassenger(AirPassenger):
    """
    Data model for a departing air passenger. It includes attributes specific to departing air passengers.
    """
            
    @computed_field(
        return_type = str,
        description = "Next Flight Destination for a departing passenger",
    )
    @property
    def next_flight_destination(cls):
        """
        Next Flight Destination for a departing passenger
        """
        return cls.previous_or_next_airport
    
    @computed_field(
        return_type = bool,
        description = "True if the next flight destination is final and not a layover",
    )
    @property
    def is_final_destination(cls):
        """
        True if the next flight destination is final and not a layover
        """
        if cls.passenger_type == e.PassengerType.DEPARTING:
            return cls.is_direct_flight
        
    final_flight_destination: NoneOrNanString[str] = Field(
        ..., description = "Final destination of the flight for departing passengers"
    )
    """
    Final destination of the flight for departing passengers.
    """

    flight_departure_time: NoneOrNan[e.DepartTime] = Field(
        ..., description = "Time of flight departure"
    )
    """
    Time of flight departure.
    """

    trip_start_time: NoneOrNan[e.DepartTime] = Field(
        ..., description="Start time of the trip"
    )
    """
    Start time of the trip.
    """

    trip_arrival_time: NoneOrNan[e.DepartTime] = Field(
        ..., description="Arrival time of the trip"
    )
    """
    Arrival time of the trip.
    """
    
class Resident(Respondent):
    """
    Data Model for a Air Passenger who is a resident of the San Deigo Region. It includes attributes specific to a Resident.
    """
    
    nights_away: NoneOrNan[e.TravelDuration] = Field(
        ..., description = "Number of nights the departing air passengers will be away"
    )
    """
    Number of nights the departing air passengers will be away.
    """

    general_use_transit_resident: NoneOrNan[e.TransitUseFrequency] = Field(
        ..., description = "General transit use frequency by residents of San Diego region in San Diego region"
    )
    """
    General transit use frequency by residents of San Diego region in San Diego region.
    """
    pass

class Visitor(Respondent):
    """
    Data Model for a visitor of the San Deigo Region. It includes attributes specific to a Visitor.
    """

    convention_center: NoneOrNanString[e.YesNoType] = Field(
        ..., description = "Whether the visitor went/going to convention center"
    )
    """
    Whether the visitor went/going to convention center.
    """

    convention_center_activity: NoneOrNanString[e.ConventionCenterActivity] = Field(
        ..., description = "Type of activity that the respondent conducted at the convention center"
    )
    """
    Type of activity that the respondent conducted at the convention center.
    """

    convention_center_activity_other: NoneOrNanString[str] = Field(
        ..., description = "Type of activity (not listed) that the respondent conducted at the convention center"
    )
    """
    Type of activity (not listed) that the respondent conducted at the convention center.
    """
    
    nights_visited: NoneOrNan[e.TravelDuration] = Field(
        ..., description = "Number of nights the arriving air passengers will be in the San Diego Region"
    )
    """
    Number of nights the arriving air passengers will be in the San Diego Region.
    """
    
    general_use_transit_visitor_home: NoneOrNan[e.TransitUseFrequency] = Field(
        ..., description = "General transit use frequency by visitors of San Diego region when home"
    )
    """
    General transit use frequency by visitors of San Diego region when home.
    """

    pass



class DepartingPassengerResident(DepartingAirPassenger, Resident):
    """
    Data Model for a departing air passenger who is a resident of the San Deigo Region. 
    """
    car_available: NoneOrNanString[e.CarAvailability] = Field(
        ..., description = "Status of car availability for the trip to the airport"
    )
    """
    Status of car availability for the trip to the airport
    """

    car_available_other: NoneOrNanString[str] = Field(
        ..., description = "Status of car availability (other than listed) for the trip to the airport"
    )
    """
    Status of car availability (other than listed) for the trip to the airport
    """
    
    reverse_mode_predicted: NoneOrNan[e.TravelMode] = Field(
        ..., description = "Mode that will be used in the reverse direction"
    )
    """
    Mode that will be used in the reverse direction.
    """

    reverse_mode_predicted_grouped: NoneOrNanString[e.TravelModeGrouped] = Field(
        ..., description = "Grouped Mode that will be used in the reverse direction")
    """
    Grouped Mode that will be used in the reverse direction
    """

    reverse_mode_predicted_other: NoneOrNanString[str] = Field(
        ..., description = "Mode (not listed) which will be used in the reverse direction"
    )
    """
    Mode (not listed) which will be used in the reverse direction
    """

    @model_validator(mode="after")
    def validate_record(cls, values):
        # Validate using SkipLogicValidator
        errors, severity_levels, num_errors = skip_logic_validator.validate("DepartingpassengerResident", values.dict())
        # Update validation fields
        #values.valid_record = len(errors) == 0
        values.validation_error = errors
        values.validation_severity = cls.determine_severity(severity_levels)
        values.validation_num_errors = num_errors
        
        return values
    
    @staticmethod
    def determine_severity(severity_levels):
        if severity_levels["Critical"] > 0:
            return "Critical"
        elif severity_levels["Non-Critical"] > 0:
            return "Non-Critical"
        return "None"
    pass 


class DepartingPassengerVisitor(DepartingAirPassenger, Visitor):

    """
    Data Model for a departing air passenger who is a resident of the San Deigo Region. 
    """

    reverse_mode: NoneOrNan[e.TravelMode] = Field(
        ..., description = "Mode that was used in the reverse direction"
    )
    """
    Mode that was used in the reverse direction.
    """

    reverse_mode_grouped: NoneOrNanString[e.TravelModeGrouped] = Field(
        ..., description = "Grouped Mode that was used in the reverse direction")
    """
    Grouped Mode that was used in the reverse direction
    """
    reverse_mode_combined: NoneOrNanString[e.TravelModeGrouped] = Field(
        ..., description = "Mode in the reverse direction")
    """
    Mode in the reverse direction.
    """

    reverse_mode_combined_other: NoneOrNanString[str] = Field(
        ..., description = "Other mode in the reverse direction")
    """
    Other mode in the reverse direction.
    """


    general_modes_used_visitor_taxi: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used Taxi as a mode during their visit to the San Diego Region"
    )
    """
    True if the visitor used Taxi as a mode during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_uber_lyft: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used Uber or Lyft as a mode during their visit to the San Diego Region"
    )
    """
    True if the visitor used Uber or Lyft as a mode during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_car_black: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used a black car service as a mode during their visit to the San Diego Region"
    )
    """
    True if the visitor used a black car service as a mode during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_dropped_off_by_family_friend: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor was dropped off by a family member or friend during their visit to the San Diego Region"
    )
    """
    True if the visitor was dropped off by a family member or friend during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_drove_alone_and_parked: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor drove alone and parked during their visit to the San Diego Region"
    )
    """
    True if the visitor drove alone and parked during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_drove_with_others_and_parked: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor drove with others and parked during their visit to the San Diego Region"
    )
    """
    True if the visitor drove with others and parked during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_rode_with_other_travelers_and_parked: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor rode with other travelers and parked during their visit to the San Diego Region"
    )
    """
    True if the visitor rode with other travelers and parked during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_coaster: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used the Coaster train during their visit to the San Diego Region"
    )
    """
    True if the visitor used the Coaster train during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_mts_red_trolley: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used the MTS Red Trolley during their visit to the San Diego Region"
    )
    """
    True if the visitor used the MTS Red Trolley during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_other_public_bus: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used other public bus services during their visit to the San Diego Region"
    )
    """
    True if the visitor used other public bus services during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_other_public_transit: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used other public transit services during their visit to the San Diego Region"
    )
    """
    True if the visitor used other public transit services during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_rental_car_dropped_off: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used a rental car and was dropped off during their visit to the San Diego Region"
    )
    """
    True if the visitor used a rental car and was dropped off during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_rental_car_parked: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used a rental car and parked during their visit to the San Diego Region"
    )
    """
    True if the visitor used a rental car and parked during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_chartered_tour_bus: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used a chartered tour bus during their visit to the San Diego Region"
    )
    """
    True if the visitor used a chartered tour bus during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_hotel_shuttle_van: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used a hotel shuttle or van during their visit to the San Diego Region"
    )
    """
    True if the visitor used a hotel shuttle or van during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_employee_shuttle: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used an employee shuttle during their visit to the San Diego Region"
    )
    """
    True if the visitor used an employee shuttle during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_other_shared_van: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used another type of shared van service during their visit to the San Diego Region"
    )
    """
    True if the visitor used another type of shared van service during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_walk: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor walked as a mode during their visit to the San Diego Region"
    )
    """
    True if the visitor walked as a mode during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_wheelchair: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used a wheelchair during their visit to the San Diego Region"
    )
    """
    True if the visitor used a wheelchair during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_bicycle_electric_bikeshare: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used an electric bicycle through a bikeshare service during their visit to the San Diego Region"
    )
    """
    True if the visitor used an electric bicycle through a bikeshare service during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_bicycle_non_electric_bikeshare: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used a non-electric bicycle through a bikeshare service during their visit to the San Diego Region"
    )
    """
    True if the visitor used a non-electric bicycle through a bikeshare service during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_bicycle_personal_electric_bicycle: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used their personal electric bicycle during their visit to the San Diego Region"
    )
    """
    True if the visitor used their personal electric bicycle during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_bicycle_personal_non_electric_bicycle: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used their personal non-electric bicycle during their visit to the San Diego Region"
    )
    """
    True if the visitor used their personal non-electric bicycle during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_e_scooter_shared: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used a shared e-scooter during their visit to the San Diego Region"
    )
    """
    True if the visitor used a shared e-scooter during their visit to the San Diego Region.
    """
    
    general_modes_used_visitor_e_scooter_personal: NoneOrNanString[bool] = Field(
        ..., description = "True if the visitor used their personal e-scooter during their visit to the San Diego Region"
    )
    """
    True if the visitor used their personal e-scooter during their visit to the San Diego Region.
    """

    general_modes_used_visitor_other: NoneOrNanString[str] = Field(
        ..., description = "Other mode used by the visitor during their visit to the San Diego Region."
    )
    """
    Other mode used by the visitor during their visit to the San Diego Region.
    """

    general_modes_used_visitor_list: NoneOrNanString[str] = Field(
        ..., description = "List of modes used by the visitor during their visit to the San Diego Region"
    )
    """
    List of modes used by the visitor during their visit to the San Diego Region
    """

    @model_validator(mode="after")
    def validate_record(cls, values):
        # Validate using SkipLogicValidator
        errors, severity_levels, num_errors = skip_logic_validator.validate("DepartingPassengerVisitor", values.dict())
        # Update validation fields
        #values.valid_record = len(errors) == 0
        values.validation_error = errors
        values.validation_severity = cls.determine_severity(severity_levels)
        values.validation_num_errors = num_errors
        
        return values
    
    @staticmethod
    def determine_severity(severity_levels):
        if severity_levels["Critical"] > 0:
            return "Critical"
        elif severity_levels["Non-Critical"] > 0:
            return "Non-Critical"
        return "None"
    pass


class ArrivingPassengerResident(ArrivingAirPassenger, Resident):
    """
    Data Model for a departing air passenger who is a resident of the San Deigo Region. 
    """
    
    reverse_mode: NoneOrNan[e.TravelMode] = Field(
        ..., description = "Mode that was used in the reverse direction"
    )
    """
    Mode that was used in the reverse direction.
    """

    @model_validator(mode="after")
    def validate_record(cls, values):
        # Validate using SkipLogicValidator
        errors, severity_levels, num_errors = skip_logic_validator.validate("ArrivingPassengerResident", values.dict())
        # Update validation fields
        #values.valid_record = len(errors) == 0
        values.validation_error = errors
        values.validation_severity = cls.determine_severity(severity_levels)
        values.validation_num_errors = num_errors
        
        return values
    
    @staticmethod
    def determine_severity(severity_levels):
        if severity_levels["Critical"] > 0:
            return "Critical"
        elif severity_levels["Non-Critical"] > 0:
            return "Non-Critical"
        return "None"
    
    pass


class ArrivingPassengerVisitor(ArrivingAirPassenger, Visitor):
    """
    Data Model for an arriving air passenger who is a visitor of the San Deigo Region. 
    """

    reverse_mode_predicted: NoneOrNan[e.TravelMode] = Field(
        ..., description = "Mode that will be used in the reverse direction"
    )
    """
    Mode that will be used in the reverse direction.
    """

    reverse_mode_predicted_other: NoneOrNanString[str] = Field(
        ..., description = "Mode (not listed) which will be used in the reverse direction"
    )
    """
    Mode (not listed) which will be used in the reverse direction
    """

    # @model_validator(mode="after")
    # def validate_missing_fields(cls, values):
    #     null_fields = [field for field, value in values if value is None and 'other' not in field]
    #     critical_fields = ['party_size_flight']
    #     if null_fields:
    #         values.valid_record = False
    #         values.validation_error = f"Missing Fields: {', '.join(null_fields)}"
    #         values.validation_num_errors = len(null_fields)
    #         if len(null_fields)>3:
    #             values.validation_severity = "High"
    #         else:
    #             values.validation_severity = "Low"
    #         if any(field in critical_fields for field in null_fields):
    #             values.validation_severity = "Critical"
    #     return values

    @model_validator(mode="after")
    def validate_record(cls, values):
        # Validate using SkipLogicValidator
        errors, severity_levels, num_errors = skip_logic_validator.validate("ArrivingPassengerVisitor", values.dict())
        
        # Update validation fields
        #values.valid_record = len(errors) == 0
        values.validation_error = errors
        values.validation_severity = cls.determine_severity(severity_levels)
        values.validation_num_errors = num_errors
        
        return values
    
    @staticmethod
    def determine_severity(severity_levels):
        if severity_levels["Critical"] > 0:
            return "Critical"
        elif severity_levels["Non-Critical"] > 0:
            return "Non-Critical"
        return "None"
    
    pass
