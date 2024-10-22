"""
Data Model for the SDIA Survey
"""

from datetime import datetime
from math import isnan
from typing import Annotated, Any, ClassVar, Literal, Optional, TypeVar, Union, List

from pydantic import (BaseModel, BeforeValidator, Field, computed_field,
                      field_validator, model_validator)
from pydantic_extra_types.coordinate import Coordinate, Latitude, Longitude

import enums as e


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


class PydanticModel(BaseModel):
    """
    Base class for all Pydantic models, create in case future modifications are helpful
    """


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

    origin_city: NoneOrNanString[str] = Field(
        ..., description="City of the origin address for the trip to the airport"
    )
    """
    City of the origin address for the trip to the airport.
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

    destination_city: NoneOrNanString[str] = Field(
        ..., description="City of the destination address from the airport"
    )
    """
    City of the destination address from the airport.
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

    shared_van_other: NoneOrNanString[str] = Field(
        ..., description = "Name of the other shared van service used by respondent"
    )
    """
    Name of the other shared van service used by respondent.
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

    taxi_fhv_fare: NoneOrNan[Union[float,str]] = Field(
        ..., description = "Taxi or for-hire vehicle fare"
    )
    """
    Taxi or for-hire vehicle fare.
    """

    taxi_fhv_wait: NoneOrNan[Union[float,str]] = Field(
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

    parking_cost_frequency: NoneOrNan[e.ParkingCostFrequency] = Field(
        ..., description = "Frequency of reported parking cost (e.g., one-time, per hour, per day, per month)"
    )
    """
    Frequency of reported parking cost (e.g., one-time, per hour, per day, per month)
    """

    parking_cost_frequency_other: NoneOrNanString[str] = Field(
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


class Respondent(PydanticModel):
    """
    Data model for a survey respondent. It includes attributes common to air passengers and employees.
    """

    respondentid: NoneOrNan[int] = Field(
        ..., description="Unique identifier for the respondent")
    """
    Unique identifier for the respondent.
    """

    date_completed: NoneOrNanString[datetime] = Field(
        ..., description = "Date and time when respondent completed the survey"
    )
    """
    Date and time when respondent completed the survey
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

    is_qualified_age: NoneOrNanString[bool] = Field(
        ...,
        description="Whether the respondent is of a qualified age to participate in the survey",
    )
    """
    Whether the respondent is of a qualified age to participate in the survey.
    """

    # is_qualified_not_connecting: NoneOrNanString[bool] = Field(
    #     ...,
    #     description="Whether the respondent is traveling to the airport and therefore qualified to participate in the survey",
    # )
    # """
    # Whether the respondent is traveling to the airport and therefore 
    # """

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

    resident_visitor: NoneOrNan[e.ResidentVisitor] = Field(
        ...,
        description="Where the respondent resides in the airport service area most of the year",
    )
    """
    Where the respondent resides in the airport service area most of the year.
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

 #Add new here
    # home_location_address: NoneOrNanString[str] =  Field(
    #     ..., description = "Street Address of the home location of the respondent"
    # )
    # """
    # Street Address of the home location of the respondent
    # """

    home_location_city: NoneOrNanString[str] =  Field(
        ..., description = "City of the home location of the respondent"
    )
    """
    City of the home location of the respondent
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

    is_income_below_poverty: NoneOrNanString[bool] = Field(
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

    stay_informed: NoneOrNanString[bool] = Field(
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
    # other_home_language: NoneOrNanString[bool] = Field(
    #     ..., description = "Does the respondent speak a language other than English at home?",
    # )
    # """
    # Does the respondent speak a language other than English at home?
    # """

    # english_proficiency: NoneOrNan[e.EnglishProficiency] = Field(
    #     ..., description="Respondent's level of English proficiency"
    # )
    # """
    # Respondent's level of English proficiency.
    # """

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
            raise (ValueError("Prefer not to disclose cannot be combined with any race"))


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

    same_commute_mode: NoneOrNanString[e.YesNoType] = Field(
        ..., description = "True if the employee always used the same travel mode to commute in the last 30 days"
    )
    """
    True if the employee always used the same travel mode to commute in the last 30 days
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


class AirPassenger(Respondent):
    """
    Data model for an air passenger respondent. It includes attributes specific to air passengers.
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
        return_type = str,
        description = "Next Flight Destination for a departing passenger",
    )
    @property
    def next_flight_destination(cls):
        """
        Next Flight Destination for a departing passenger
        """
        if cls.passenger_type == e.PassengerType.DEPARTING:
            return cls.previous_or_next_airport

    # next_flight_destination: NoneOrNanString[str] = Field(
    #     ..., description = "Destination of the flight for departing passengers"
    # )
    # """
    # Destination of the flight for departing passengers.
    # """

    # previous_flight_origin: NoneOrNanString[str] = Field(
    #     ..., description = "Origin of the flight for arriving passengers"
    # )
    # """
    # Origin of the flight for arriving passengers.
    # """

    airline: NoneOrNanString[int] = Field(
        ..., description = "Airline of the respondent's flight"
    )
    """
    Airline of the respondent's flight.
    """

    flight_number: NoneOrNanString[Union[str, int]] = Field(
        ..., description = "Flight number of the respondent's flight"
    )
    """
    Flight number of the respondent's flight.
    """

    not_using_connecting: NoneOrNanString[bool] =  Field(
        ..., description = "True if the passenger did not use/is not using any connecting flights in their journey"
    )
    """
    True if the passenger did not use/is not using any connecting flights in their journey
    """


    @computed_field(
        return_type = bool,
        description = "True if the previous flight origin was original and not a layover",
    )
    @property
    def is_original_origin(cls):
        """
        True if the previous flight origin was original and not a layover
        """
        if cls.passenger_type == e.PassengerType.ARRIVING:
            return cls.not_using_connecting
        
        
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
            return cls.not_using_connecting
        


    # is_final_destination: NoneOrNanString[bool] = Field(
    #     ..., description = "Whether respondent's next destination is their final destination"
    # )
    # """
    # Whether respondent's next destination is their final destination.
    # """

    # is_original_origin: NoneOrNanString[bool] = Field(
    #     ..., description = "Whether the respondent used a connecting flight"
    # )
    # """
    # Whether the respondent used a connecting flight.
    # """

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

    convention_center: NoneOrNanString[bool] = Field(
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

    nights_away: NoneOrNan[e.TravelDuration] = Field(
        ..., description = "Number of nights the departing air passengers will be away"
    )
    """
    Number of nights the departing air passengers will be away.
    """

    nights_visited: NoneOrNan[e.TravelDuration] = Field(
        ..., description = "Number of nights the arriving air passengers will be in the San Diego Region"
    )
    """
    Number of nights the arriving air passengers will be in the San Diego Region.
    """

    party_size_flight: NoneOrNanString[e.PartySize] = Field(
        ..., description = "Size of the party flying with the respondent (count includes the respondent)"
    )
    """
    Size of the party flying with the respondent (count includes the respondent).
    """

    party_size_ground_access_same: NoneOrNanString[bool] = Field(
        ..., description = "Whether flying party all traveled to airport together"
    )
    """
    Whether flying party all traveled to airport together
    """

    party_size_ground_access: NoneOrNanString[e.PartySize] = Field(
        ..., description = "Size of ground access travel party"
    )
    """
    Size of ground access travel party.
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


#Add here
    sdia_flight_frequency: NoneOrNan[e.SanFlightFrequency] = Field(
        ..., description = "Respondent's number of flights from SDIA in the past 12 months"
    )
    """
    Respondent's number of flights from SDIA in the past 12 months.
    """

    sdia_previous_accessmode: NoneOrNan[e.SanFlightFrequency] = Field(
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

#
    sdia_accessmode_decision: NoneOrNan[e.ModeDecision] = Field(
        ..., description = "Factor which affects mode choice, for respondents who do not always used the same mode"
    )
    """
    Factor which affects mode choice, for respondents who do not always used the same mode.
    """

    reverse_mode: NoneOrNan[e.TravelMode] = Field(
        ..., description = "Mode that was used in the reverse direction"
    )
    """
    Mode that was used in the reverse direction.
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

    general_use_transit_resident: NoneOrNan[e.TransitUseFrequency] = Field(
        ..., description = "General transit use frequency by residents of San Diego region in San Diego region"
    )
    """
    General transit use frequency by residents of San Diego region in San Diego region.
    """

    general_use_transit_visitor_home: NoneOrNan[e.TransitUseFrequency] = Field(
        ..., description = "General transit use frequency by visitors of San Diego region when home"
    )
    """
    General transit use frequency by visitors of San Diego region when home.
    """

    # general_modes_used_visitor: List[NoneOrNan[e.TravelMode]] = Field(
    #     ..., description = "Modes respondent used during visit of San Diego region"
    # )
    # """
    # Modes respondent used during visit of San Diego region.
    # """

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

    airport_access_transit_use_elsewhere: NoneOrNanString[e.OtherFlightAndTransitUseFrequency] = Field(
        ..., description = "Frequency of Transit use by respondent to access other airports"
    )
    """
    Frequency of Transit use by respondent to access other airports.
    """

    airportaccesstransitname: NoneOrNanString[str] = Field(
        ..., description = "Names of airports accessed by transit"
    )
    """
    Names of airports accessed by transit.
    """

