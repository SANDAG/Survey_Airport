from enum import Enum, IntEnum

from utils import military_to_clock

class InterviewLocation(IntEnum):
    """
    Integer Mapping for interview locations
    """
    TERMINAL_1 = 1
    TERMINAL_2 = 2
    ONBOARD_992 = 3
    ONBOARD_FLYER = 4
    RENTAL_CENTER = 5
    PASSENGER_PARKING = 6
    EMPLOYEE_PARKING = 7
    OTHER_SPECIFY = 98


class InboundOutbound(IntEnum):
    """
    Integer mapping for inbound and outbound flights
    """

    INBOUND_TO_AIRPORT = 1
    OUTBOUND_FROM_AIRPORT = 2


class Type(IntEnum):
    """
    Integer mapping for market segmentation
    """

    PASSENGER = 1
    EMPLOYEE = 2
    OTHER_SPECIFY = 98


class PassengerType(IntEnum):
    """
    Integer Mapping for type of passenger
    """

    ARRIVING = 1
    DEPARTING = 2
    CONNECTING = 3


class ResidentVisitorGeneral(IntEnum):
    """
    Integer Mapping for the respondent if they are resident, visitor or neither. First option if departing, second if arriving
    """
    GOING_HOME_OR_VISITING = 1
    LEAVING_HOME_OR_COMING_HOME = 2
    NEITHER = 3


class ResidentVisitor(IntEnum):
    """
    Integer Mapping for Residence Zones
    """
    SAN_DIEGO_REGION = 1
    OTHER_SOUTHERN_CALIFORNIA = 2
    OTHER_CALIFORNIA = 3
    TIJUANA_REGION = 4
    OTHER_BAJA_CALIFORNIA = 5
    OTHER_STATE_US = 6
    OTHER_STATE_MEXICO = 7
    NONE_OF_THE_ABOVE = 8
    OTHER = 98
    REFUSED = 99


class Country(IntEnum):
    """
    Integer Mapping for all the countries in the world
    """
    UNITED_STATES = 1
    MEXICO = 2
    AFGHANISTAN = 3
    ALBANIA = 4
    ALGERIA = 5
    ANDORRA = 6
    ANGOLA = 7
    ANTIGUA_AND_BARBUDA = 8
    ARGENTINA = 9
    ARMENIA = 10
    AUSTRALIA = 11
    AUSTRIA = 12
    AZERBAIJAN = 13
    BAHAMAS = 14
    BAHRAIN = 15
    BANGLADESH = 16
    BARBADOS = 17
    BELARUS = 18
    BELGIUM = 19
    BELIZE = 20
    BENIN = 21
    BHUTAN = 22
    BOLIVIA = 23
    BOSNIA_AND_HERZEGOVINA = 24
    BOTSWANA = 25
    BRAZIL = 26
    BRUNEI = 27
    BULGARIA = 28
    BURKINA_FASO = 29
    BURUNDI = 30
    COTE_DIVOIRE = 31
    CABO_VERDE = 32
    CAMBODIA = 33
    CAMEROON = 34
    CANADA = 35
    CENTRAL_AFRICAN_REPUBLIC = 36
    CHAD = 37
    CHILE = 38
    CHINA = 39
    COLOMBIA = 40
    COMOROS = 41
    CONGO_CONGO_BRAZZAVILLE = 42
    COSTA_RICA = 43
    CROATIA = 44
    CUBA = 45
    CYPRUS = 46
    CZECHIA_CZECH_REPUBLIC = 47
    DEMOCRATIC_REPUBLIC_OF_THE_CONGO = 48
    DENMARK = 49
    DJIBOUTI = 50
    DOMINICA = 51
    DOMINICAN_REPUBLIC = 52
    ECUADOR = 53
    EGYPT = 54
    EL_SALVADOR = 55
    EQUATORIAL_GUINEA = 56
    ERITREA = 57
    ESTONIA = 58
    ESWATINI_FMR_SWAZILAND = 59
    ETHIOPIA = 60
    FIJI = 61
    FINLAND = 62
    FRANCE = 63
    GABON = 64
    GAMBIA = 65
    GEORGIA = 66
    GERMANY = 67
    GHANA = 68
    GREECE = 69
    GRENADA = 70
    GUATEMALA = 71
    GUINEA = 72
    GUINEA_BISSAU = 73
    GUYANA = 74
    HAITI = 75
    HOLY_SEE = 76
    HONDURAS = 77
    HUNGARY = 78
    ICELAND = 79
    INDIA = 80
    INDONESIA = 81
    IRAN = 82
    IRAQ = 83
    IRELAND = 84
    ISRAEL = 85
    ITALY = 86
    JAMAICA = 87
    JAPAN = 88
    JORDAN = 89
    KAZAKHSTAN = 90
    KENYA = 91
    KIRIBATI = 92
    KUWAIT = 93
    KYRGYZSTAN = 94
    LAOS = 95
    LATVIA = 96
    LEBANON = 97
    LESOTHO = 98
    LIBERIA = 99
    LIBYA = 100
    LIECHTENSTEIN = 101
    LITHUANIA = 102
    LUXEMBOURG = 103
    MADAGASCAR = 104
    MALAWI = 105
    MALAYSIA = 106
    MALDIVES = 107
    MALI = 108
    MALTA = 109
    MARSHALL_ISLANDS = 110
    MAURITANIA = 111
    MAURITIUS = 112
    MICRONESIA = 113
    MOLDOVA = 114
    MONACO = 115
    MONGOLIA = 116
    MONTENEGRO = 117
    MOROCCO = 118
    MOZAMBIQUE = 119
    MYANMAR_FORMERLY_BURMA = 120
    NAMIBIA = 121
    NAURU = 122
    NEPAL = 123
    NETHERLANDS = 124
    NEW_ZEALAND = 125
    NICARAGUA = 126
    NIGER = 127
    NIGERIA = 128
    NORTH_KOREA = 129
    NORTH_MACEDONIA = 130
    NORWAY = 131
    OMAN = 132
    PAKISTAN = 133
    PALAU = 134
    PALESTINE_STATE = 135
    PANAMA = 136
    PAPUA_NEW_GUINEA = 137
    PARAGUAY = 138
    PERU = 139
    PHILIPPINES = 140
    POLAND = 141
    PORTUGAL = 142
    QATAR = 143
    ROMANIA = 144
    RUSSIA = 145
    RWANDA = 146
    SAINT_KITTS_AND_NEVIS = 147
    SAINT_LUCIA = 148
    SAINT_VINCENT_AND_THE_GRENADINES = 149
    SAMOA = 150
    SAN_MARINO = 151
    SAO_TOME_AND_PRINCIPE = 152
    SAUDI_ARABIA = 153
    SENEGAL = 154
    SERBIA = 155
    SEYCHELLES = 156
    SIERRA_LEONE = 157
    SINGAPORE = 158
    SLOVAKIA = 159
    SLOVENIA = 160
    SOLOMON_ISLANDS = 161
    SOMALIA = 162
    SOUTH_AFRICA = 163
    SOUTH_KOREA = 164
    SOUTH_SUDAN = 165
    SPAIN = 166
    SRI_LANKA = 167
    SUDAN = 168
    SURINAME = 169
    SWEDEN = 170
    SWITZERLAND = 171
    SYRIA = 172
    TAJIKISTAN = 173
    TANZANIA = 174
    THAILAND = 175
    TIMOR_LESTE = 176
    TOGO = 177
    TONGA = 178
    TRINIDAD_AND_TOBAGO = 179
    TUNISIA = 180
    TURKEY = 181
    TURKMENISTAN = 182
    TUVALU = 183
    UGANDA = 184
    UKRAINE = 185
    UNITED_ARAB_EMIRATES = 186
    UNITED_KINGDOM = 187
    URUGUAY = 188
    UZBEKISTAN = 189
    VANUATU = 190
    VENEZUELA = 191
    VIETNAM = 192
    YEMEN = 193
    ZAMBIA = 194
    ZIMBABWE = 195


class State(IntEnum):
    """
    Integer mapping for all US and Mexico States
    """
    ALABAMA = 1
    ALASKA = 2
    AMERICAN_SAMOA = 3
    ARIZONA = 4
    ARKANSAS = 5
    CALIFORNIA = 6
    COLORADO = 7
    CONNECTICUT = 8
    DELAWARE = 9
    DISTRICT_OF_COLUMBIA = 10
    FLORIDA = 11
    GEORGIA = 12
    GUAM = 13
    HAWAII = 14
    IDAHO = 15
    ILLINOIS = 16
    INDIANA = 17
    IOWA = 18
    KANSAS = 19
    KENTUCKY = 20
    LOUISIANA = 21
    MAINE = 22
    MARYLAND = 23
    MASSACHUSETTS = 24
    MICHIGAN = 25
    MINNESOTA = 26
    MISSISSIPPI = 27
    MISSOURI = 28
    MONTANA = 29
    NEBRASKA = 30
    NEVADA = 31
    NEW_HAMPSHIRE = 32
    NEW_JERSEY = 33
    NEW_MEXICO = 34
    NEW_YORK = 35
    NORTH_CAROLINA = 36
    NORTH_DAKOTA = 37
    NORTHERN_MARIANA_ISLANDS = 38
    OHIO = 39
    OKLAHOMA = 40
    OREGON = 41
    PENNSYLVANIA = 42
    PUERTO_RICO = 43
    RHODE_ISLAND = 44
    SOUTH_CAROLINA = 45
    SOUTH_DAKOTA = 46
    TENNESSEE = 47
    TEXAS = 48
    UTAH = 49
    VERMONT = 50
    VIRGINIA = 51
    VIRGIN_ISLANDS = 52
    WASHINGTON = 53
    WEST_VIRGINIA = 54
    WISCONSIN = 55
    WYOMING = 56
    AGUASCALIENTES = 57
    BAJA_CALIFORNIA = 58
    BAJA_CALIFORNIA_SUR = 59
    CAMPECHE = 60
    CHIAPAS = 61
    CHIHUAHUA = 62
    COAHUILA = 63
    COLIMA = 64
    CIUDAD_DE_MEXICO = 65
    DURANGO = 66
    GUANAJUATO = 67
    GUERRERO = 68
    HIDALGO = 69
    JALISCO = 70
    MEXICO_STATE = 71
    MICHOACAN = 72
    MORELOS = 73
    NAYARIT = 74
    NUEVO_LEON = 75
    OAXACA = 76
    PUEBLA = 77
    QUERETARO = 78
    QUINTANA_ROO = 79
    SAN_LUIS_POTOSI = 80
    SINALOA = 81
    SONORA = 82
    TABASCO = 83
    TAMAULIPAS = 84
    TLAXCALA = 85
    VERACRUZ = 86
    YUCATAN = 87
    ZACATECAS = 88
    NOT_US_OR_MEXICO_RESIDENT = 99


class Terminal(IntEnum):
    """
    Integer mapping for terminals

    """
    TERMINAL_1 = 1
    TERMINAL_2 = 2


class Airline(IntEnum):
    """
    Integer Mapping for airlines at SAN
    """
    AIR_CANADA = 1
    ALASKA_AIRLINES = 2
    ALLEGIANT_AIR = 3
    AMERICAN_AIRLINES = 4
    BREEZE = 5
    BRITISH_AIRWAYS = 6
    DELTA_AIRLINES = 7
    HAWAIIAN_AIRLINES = 8
    JAPAN_AIRLINES = 9
    JETBLUE = 10
    LUFTHANSHA = 11
    UNITED_AIRLINES = 12
    WESTJET = 13
    FRONTIER_AIRLINES = 14
    SOUTHWEST_AIRLINES = 15
    SPIRIT = 16
    SUNCOUNTY_AIRLINES = 17
    OTHER_SPECIFY = 98


class DepartTime(IntEnum):  
    """
    Integer mapping for time categories
    """

    FIVE_TO_FIVE_THIRTY = 1
    FIVE_THIRTY_TO_SIX = 2
    SIX_TO_SIX_THIRTY = 3
    SIX_THIRTY_TO_SEVEN = 4
    SEVEN_TO_SEVEN_THIRTY = 5
    SEVEN_THIRTY_TO_EIGHT = 6
    EIGHT_TO_EIGHT_THIRTY = 7
    EIGHT_THIRTY_TO_NINE = 8
    NINE_TO_NINE_THIRTY = 9
    NINE_THIRTY_TO_TEN = 10
    TEN_TO_TEN_THIRTY = 11
    TEN_THIRTY_TO_ELEVEN = 12
    ELEVEN_TO_ELEVEN_THIRTY = 13
    ELEVEN_THIRTY_TO_NOON = 14
    NOON_TO_TWELVE_THIRTY = 15
    TWELVE_THIRTY_TO_THIRTEEN = 16
    THIRTEEN_TO_THIRTEEN_THIRTY = 17
    THIRTEEN_THIRTY_TO_FOURTEEN = 18
    FOURTEEN_TO_FOURTEEN_THIRTY = 19
    FOURTEEN_THIRTY_TO_FIFTEEN = 20
    FIFTEEN_TO_FIFTEEN_THIRTY = 21
    FIFTEEN_THIRTY_TO_SIXTEEN = 22
    SIXTEEN_TO_SIXTEEN_THIRTY = 23
    SIXTEEN_THIRTY_TO_SEVENTEEN = 24
    SEVENTEEN_TO_SEVENTEEN_THIRTY = 25
    SEVENTEEN_THIRTY_TO_EIGHTEEN = 26
    EIGHTEEN_TO_EIGHTEEN_THIRTY = 27
    EIGHTEEN_THIRTY_TO_NINETEEN = 28
    NINETEEN_TO_NINETEEN_THIRTY = 29
    NINETEEN_THIRTY_TO_TWENTY = 30
    TWENTY_TO_TWENTY_THIRTY = 31
    TWENTY_THIRTY_TO_TWENTY_ONE = 32
    TWENTY_ONE_TO_TWENTY_ONE_THIRTY = 33
    TWENTY_ONE_THIRTY_TO_TWENTY_TWO = 34
    TWENTY_TWO_TO_TWENTY_TWO_THIRTY = 35
    TWENTY_TWO_THIRTY_TO_TWENTY_THREE = 36
    TWENTY_THREE_TO_TWENTY_THREE_THIRTY = 37
    TWENTY_THREE_THIRTY_TO_MIDNIGHT = 38
    MIDNIGHT_TO_ZERO_THIRTY = 39
    ZERO_THIRTY_TO_ONE = 40
    ONE_TO_ONE_THIRTY = 41
    ONE_THIRTY_TO_TWO = 42
    TWO_TO_TWO_THIRTY = 43
    TWO_THIRTY_TO_THREE = 44
    THREE_TO_THREE_THIRTY = 45
    THREE_THIRTY_TO_FOUR = 46
    FOUR_TO_FOUR_THIRTY = 47
    FOUR_THIRTY_TO_FIVE = 48



class FlightPurpose(IntEnum):
    """
    Integer Mapping for Flight Purposes
    """
    BUSINESS_WORK = 1
    LEISURE_FAMILY = 2
    COMBINATION_BUSINESS_LEISURE = 3
    PERSONAL = 4
    SCHOOL = 5
    COMMUTE = 6
    OTHER_SPECIFY = 98


class ConventionCenterActivity(IntEnum):
    """
    Integer mapping for convention center activities
    """
    ATTENDEE = 1
    EXHIBITOR = 2
    MEETING_PLANNER = 3
    CONTRACTOR = 4
    OTHER_SPECIFY = 98
    NOT_APPLICABLE = 99


class CheckedBags(IntEnum):
    """
    Integer mapping for number of checked bags
    """
    NONE = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT_OR_MORE = 8


class CarryOns(IntEnum):
    """
    Integer mapping for number of carryon bags
    """
    NONE = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT_OR_MORE = 8


class TravelDuration(IntEnum):
    """
    Integer Mapping for travel duration (nights away or nights visited)
    """
    NONE = 1
    ONE = 2
    TWO = 3
    THREE = 4
    FOUR = 5
    FIVE = 6
    SIX = 7
    SEVEN = 8
    EIGHT_TO_TEN = 9
    ELEVEN_TO_FOURTEEN = 10
    MORE_THAN_FOURTEEN = 11


class PartySize(IntEnum):
    """
    Integer mapping for number of persons in travel party
    """
    ONE = 1  
    TWO = 2
    THREE = 3
    FOUR = 4    
    FIVE = 5
    SIX = 6
    SEVEN_OR_MORE = 7


class SanBuildings(IntEnum):
    """
    Integer mapping for SAN Airport buildings

    """

    TERMINAL_1 = 1 
    TERMINAL_2 = 2 
    SDCRAA_ADMIN_BLDG = 3
    QHP_LIBERTY_STATION = 4 
    SDCRAA_ADC_TRAILERS = 5 
    AIRLINE_SUPPORT_BLDG_HARBOR_DRIVE = 6
    AIR_CARGO_NORTH = 7
    RENTAL_CAR_CENTER = 8
    RECEIVING_DISTRIBUTION_CENTER = 9 
    SIGNATURE_FLIGHT_SUPPORT = 10
    FACILITIES_MAINTENANCE = 11
    FBO = 12
    MENZIES = 13
    FAA = 14
    OTHER_SPECIFY = 98
    REFUSED = 99


class Employers(IntEnum):
    """
    Integer mapping for employers

    """
    AIR_CANADA = 1	
    ALASKA_AIRLINES = 2	
    ALLEGIANT_AIR = 3	
    AMERICAN_AIRLINES = 4	
    ARTISAN_MARKET = 5	
    ASIAN_KITCHEN = 6	
    ASPIRE_LOUNGE = 7	
    BANKERS_HILL_BAR_AND_MARKET = 8	
    BAY_BOOKS_OF_CORONADO = 9	
    BE_RELAX_SPA = 10	
    BEAUDEVIN_VINE_AND_TAPAS_BAR = 11	
    BRITISH_AIRWAYS = 12	
    BROOKSTONE = 13	
    BUBBLES_SEAFOOD_AND_WINE_BAR = 14	
    CALIFORNIA_PIZZA_KITCHEN = 15	
    CAMDEN_FOOD_CO = 16	
    CIAO_GOURMET_MARKET = 17	
    CNBC_EXPRESS = 18	
    CNBC_NEWS_SAN_DIEGO = 19	
    DARK_HORSE_COFFEE_ROASTERS = 20	
    DELTA_AIRLINES = 21	
    DELTA_SKY_CLUB = 22	
    DISCOVER_SAN_DIEGO = 23	
    EINSTEIN_BROS_BAGELS = 24	
    ELEGANT_DESSERTS = 25	
    FRONTIER_AIRLINES = 26	
    GASLAMP_MARKETPLACE = 27	
    HAWAIIAN_AIRLINES = 28	
    HUDSON_NEWS = 29	
    INMOTION_ENTERTAINMENT = 30	
    JACK_IN_THE_BOX = 31	
    JAPAN_AIRLINES = 32	
    JETBLUE = 33	
    JETBOX = 34	
    JETBOX_MARKET = 35	
    KUSI_NEWS = 36	
    LINDBERGH_FIELD_NEWS = 37	
    LUFTHANSA = 38	
    OLD_TOWN_NEWS_AND_MARKET = 39	
    PACIFICA_BREEZE_CAFE = 40	
    PANDA_EXPRESS = 41	
    PANNIKIN_COFFEE_AND_TEA = 42	
    PEETS_COFFEE_AND_TEA = 43	
    PGA_TOUR_GRILL = 44	
    PGA_TOUR_SHOP = 45	
    PHILS_BBQ = 46	
    PRADO_AT_THE_AIRPORT = 47	
    QDOBA_MEXICAN_GRILL = 48	
    RED_MANGO = 49	
    RIP_CURL = 50	
    SAN_LIFE_MARKET = 51	
    SAND_NEWS = 52	
    SKY_FREE_SHOP = 53	
    SOUNDBALANCE = 54	
    SOUTHWEST_AIRLINES = 55	
    SPIRIT = 56	
    STARBUCKS = 57	
    STELLAR_NEWS_EXPRESS = 58	
    STONE_BREWING_COMPANY = 59	
    SUNCOUNTY_AIRLINES = 60	
    SUNGLASS_HUT = 61	
    SWAROVSKI = 62	
    TECH_ON_THE_GO = 63	
    THE_BEACH_HOUSE = 64	
    THE_COUNTER_CUSTOM_BUILT_BURGERS = 65	
    TOMMY_VS_PIZZERIA = 66	
    TRANSPORTATION_SECURITY_ADMINISTRATION_TSA = 67	
    UNITED_AIRLINES = 68	
    UNITED_CLUB = 69	
    UNITED_SERVICE_ORGANIZATIONS = 70	
    URBAN_CRAVE = 71	
    US_CUSTOMS_AND_BORDER_PROTECTION = 72	
    US_NEWS_AND_WORLD_REPORT = 73	
    WARWICKS_OF_LA_JOLLA = 74	
    WESTJET = 75	
    OTHER_SEPCIFY = 98	


class Occupations(IntEnum):
    """
    Integer mapping for occupations

    """

    AIRCRAFT_MECHANIC = 1
    PILOT = 2
    AIRCRAFT_SVC_ATTENDANT = 3
    AIR_TRAFFIC_CONTROLLER = 4
    FLIGHT_ATTENDANT = 5
    TICKET_AGENT = 6
    CARGO_AGENT = 7
    CARGO_HANDLER = 8
    BLDG_MAINTENANCE_CLEANING = 9
    PARKING_ATTENDANT = 10
    DRIVER = 11
    TSA = 12
    LAW_ENFORCEMENT = 13
    GENERAL_AND_OPERATIONS_MANAGERS = 14
    PROGRAM_AND_PROJECT_MANAGERS = 15
    RETAIL_RESTAURANT = 16
    CONSTRUCTION = 17
    OTHER_LABORERS = 18
    OTHER_CUSTOMER_SUPPORT = 19
    OTHER_ADMIN_SUPPORT = 20
    OTHER_SPECIFY = 98
    REFUSED = 99


class HoursWorked(IntEnum):
    """
    Integer mapping for number of hours employee works at SAN
    """

    ZERO = 1
    ONE_TO_TEN = 2
    ELEVEN_TO_TWENTY = 3
    TWENTY_ONE_TO_THIRTY = 4
    THIRTY_ONE_TO_FORTY = 5
    FORTY_ONE_TO_FIFTY = 6
    FIFTY_ONE_TO_SIXTY = 7
    SIXTY_ONE_TO_SEVENTY = 8
    SEVENTY_ONE_TO_EIGHTY = 9
    MORE_THAN_EIGHTY = 10
    OTHER = 98
    REFUSED = 99


class CommuteDays(IntEnum):
    """
    Integer mapping for number of days employee commutes to SAN
    """

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    OTHER = 98
    REFUSED = 99


class ShiftTime(Enum):
    class TimeRange:
        """ Make time ranges for categorization."""

        def __init__(self, lower_military_time, upper_military_time):
            self.lower_military_time = lower_military_time
            self.upper_military_time = upper_military_time

        def __str__(self):
            lower_clock_time = military_to_clock(self.lower_military_time)
            upper_clock_time = military_to_clock(self.upper_military_time)
            return f"{lower_clock_time} - {upper_clock_time}"

    ZERO_TO_ZERO_THIRTY = TimeRange("0000", "0030")
    ZERO_THIRTY_TO_ZERO_ONE = TimeRange("0030", "0100")
    ZERO_ONE_TO_ZERO_ONE_THIRTY = TimeRange("0100", "0130")
    ZERO_ONE_THIRTY_TO_ZERO_TWO = TimeRange("0130", "0200")
    ZERO_TWO_TO_ZERO_TWO_THIRTY = TimeRange("0200", "0230")
    ZERO_TWO_THIRTY_TO_ZERO_THREE = TimeRange("0230", "0300")
    ZERO_THREE_TO_ZERO_THREE_THIRTY = TimeRange("0300", "0330")
    ZERO_THREE_THIRTY_TO_ZERO_FOUR = TimeRange("0330", "0400")
    ZERO_FOUR_TO_ZERO_FOUR_THIRTY = TimeRange("0400", "0430")
    ZERO_FOUR_THIRTY_TO_ZERO_FIVE = TimeRange("0430", "0500")
    ZERO_FIVE_TO_ZERO_FIVE_THIRTY = TimeRange("0500", "0530")
    ZERO_FIVE_THIRTY_TO_ZERO_SIX = TimeRange("0530", "0600")
    ZERO_SIX_TO_ZERO_SIX_THIRTY = TimeRange("0600", "0630")
    ZERO_SIX_THIRTY_TO_ZERO_SEVEN = TimeRange("0630", "0700")
    ZERO_SEVEN_TO_ZERO_SEVEN_THIRTY = TimeRange("0700", "0730")
    ZERO_SEVEN_THIRTY_TO_ZERO_EIGHT = TimeRange("0730", "0800")
    ZERO_EIGHT_TO_ZERO_EIGHT_THIRTY = TimeRange("0800", "0830")
    ZERO_EIGHT_THIRTY_TO_ZERO_NINE = TimeRange("0830", "0900")
    ZERO_NINE_TO_ZERO_NINE_THIRTY = TimeRange("0900", "0930")
    ZERO_NINE_THIRTY_TO_ZERO_TEN = TimeRange("0930", "1000")
    TEN_TO_TEN_THIRTY = TimeRange("1000", "1030")
    TEN_THIRTY_TO_ELEVEN = TimeRange("1030", "1100")
    ELEVEN_TO_ELEVEN_THIRTY = TimeRange("1100", "1130")
    ELEVEN_THIRTY_TO_NOON = TimeRange("1130", "1200")
    NOON_TO_TWELVE_THIRTY = TimeRange("1200", "1230")
    TWELVE_THIRTY_TO_THIRTEEN_HUNDRED = TimeRange("1230", "1300")
    THIRTEEN_HUNDRED_TO_THIRTEEN_THIRTY = TimeRange("1300", "1330")
    THIRTEEN_THIRTY_TO_FOURTEEN_HUNDRED = TimeRange("1330", "1400")
    FOURTEEN_HUNDRED_TO_FOURTEEN_THIRTY = TimeRange("1400", "1430")
    FOURTEEN_THIRTY_TO_FIFTEEN_HUNDRED = TimeRange("1430", "1500")
    FIFTEEN_HUNDRED_TO_FIFTEEN_THIRTY = TimeRange("1500", "1530")
    FIFTEEN_THIRTY_TO_SIXTEEN_HUNDRED = TimeRange("1530", "1600")
    SIXTEEN_HUNDRED_TO_SIXTEEN_THIRTY = TimeRange("1600", "1630")
    SIXTEEN_THIRTY_TO_SEVENTEEN_HUNDRED = TimeRange("1630", "1700")
    SEVENTEEN_HUNDRED_TO_SEVENTEEN_THIRTY = TimeRange("1700", "1730")
    SEVENTEEN_THIRTY_TO_EIGHTEEN_HUNDRED = TimeRange("1730", "1800")
    EIGHTEEN_HUNDRED_TO_EIGHTEEN_THIRTY = TimeRange("1800", "1830")
    EIGHTEEN_THIRTY_TO_NINETEEN_HUNDRED = TimeRange("1830", "1900")
    NINETEEN_HUNDRED_TO_NINETEEN_THIRTY = TimeRange("1900", "1930")
    NINETEEN_THIRTY_TO_TWENTY_HUNDRED = TimeRange("1930", "2000")
    TWENTY_HUNDRED_TO_TWENTY_THIRTY = TimeRange("2000", "2030")
    TWENTY_THIRTY_TO_TWENTY_ONE_HUNDRED = TimeRange("2030", "2100")
    TWENTY_ONE_HUNDRED_TO_TWENTY_ONE_THIRTY = TimeRange("2100", "2130")
    TWENTY_ONE_THIRTY_TO_TWENTY_TWO_HUNDRED = TimeRange("2130", "2200")
    TWENTY_TWO_HUNDRED_TO_TWENTY_TWO_THIRTY = TimeRange("2200", "2230")
    TWENTY_TWO_THIRTY_TO_TWENTY_THREE_HUNDRED = TimeRange("2230", "2300")
    TWENTY_THREE_HUNDRED_TO_TWENTY_THREE_THIRTY = TimeRange("2300", "2330")
    TWENTY_THREE_THIRTY_TO_MIDNIGHT = TimeRange("2330", "0000")


class TravelMode(Enum):
    """
    Mapping for all the modes used in the survey
    """
    WALK = (1, "Walk")
    WHEELCHAIR_OR_MOBILITY_DEVICE = (2, "Wheelchair or other mobility device")
    BICYCLE_ELECTRIC_BIKESHARE = (3, "Bicycle: electric bikeshare")
    BICYCLE_NON_ELECTRIC_BIKESHARE = (4, "Bicycle: non-electric bikeshare")
    E_SCOOTER_SHARED = (5, "E-scooter: shared")
    BICYCLE_PERSONAL_ELECTRIC = (6, "Bicycle: personal electric bicycle")
    BICYCLE_PERSONAL_NON_ELECTRIC = (7, "Bicycle: personal non-electric bicycle")
    E_SCOOTER_PERSONAL = (8, "E-scooter: personal")
    TAXI = (9, "Taxi")
    UBER_LYFT = (10, "Uber/Lyft")
    CAR_SERVICE_BLACK_LIMO = (11, "Car service/black car/limo/executive car")
    DROPPED_OFF_BY_FAMILY_FRIEND = (12, "Dropped off by car by family/friend")
    DROVE_ALONE_AND_PARKED = (13, "Drove alone and parked")
    DROVE_WITH_OTHERS_AND_PARKED = (14, "Drove with others and parked")
    MTS_ROUTE_992 = (15, "MTS Route 992")
    AIRPORT_FLYER_SHUTTLE = (16, "Airport Flyer Shuttle")
    CHARTERED_TOUR_BUS = (17, "Chartered tour bus")
    EMPLOYEE_SHUTTLE = (18, "Employee shuttle")
    RENTAL_CAR_DROPPED_OFF = (19, "Rental car: Dropped off at rental agency")
    RENTAL_CAR_PARKED = (20, "Rental car: parked rental car")
    HOTEL_SHUTTLE_VAN = (21, "Hotel shuttle van")
    OTHER_SHARED_VAN = (22, "Other shared van (please specify)")
    PICKED_UP_BY_FAMILY_FRIEND = (23, "Picked up by car by family/friend")
    GET_IN_PARKED_VEHICLE_AND_DRIVE_ALONE = (24, "Get in a parked vehicle and drive alone")
    GET_IN_PARKED_VEHICLE_AND_DRIVE_WITH_OTHERS = (25, "Get in a parked vehicle and drive with others")
    GET_IN_PARKED_VEHICLE_AND_RIDE_WITH_OTHER_TRAVELERS = (26, "Get in a parked vehicle and ride with other traveler(s)")
    RENTAL_CAR_PICKED_UP = (27, "Rental car: Picked up at rental agency")
    RENTAL_CAR_GET_IN_PARKED = (28, "Rental car: get in a parked rental car")
    RODE_WITH_OTHER_TRAVELERS_AND_PARKED = (29, "Rode with other traveler(s) and parked")
    OTHER_PUBLIC_TRANSIT = (30, "Other public transit")
    OTHER = (98, "Other")
    REFUSED_NO_ANSWER = (99, "Refused/No Answer")


class BusRoutes(Enum):
    """
    Enum Mappings for MTS Bus Routes
    """
    MTS_4_12TH_IMPERIAL_TROLLEY_LOMITA_VILLAGE = "MTS_1_4"
    MTS_AIR_OLD_TOWN_TO_AIRPORT_SHUTTLE = "MTS_1_AIR"
    MTS_7_DOWNTOWN_SAN_DIEGO_UNIVERSITY_COLLEGE = "MTS_1_7"
    MTS_41_FASHION_VALLEY_UCSD = "MTS_1_41"
    MTS_964_MIRA_MESA_ALLIANT_UNIVERSITY_VIA_MCTS = "MTS_1_964"
    MTS_8_OLD_TOWN_BALBOA_AV_TC = "MTS_1_8"
    MTS_992_AIRPORT_DOWNTOWN_SHUTTLE = "MTS_1_992"
    MTS_1_FASHION_VALLEY_LA_MESA = "MTS_1_1"
    MTS_709_H_ST_TRANSIT_CENTER_OTAY_RANCH_TOWN_CENTER = "MTS_1_709"
    MTS_901_IRIS_TRANSIT_CENTER_DOWNTOWN_SAN_DIEGO = "MTS_1_901"
    MTS_BLUE_SAN_YSIDRO_UTC = "MTS_1_Blue"
    MTS_5_DOWNTOWN_SAN_DIEGO_EUCLID_TRANSIT_CENTER = "MTS_1_5"
    MTS_235_DOWNTOWN_ESCONDIDO_TRANSIT_CENTER = "MTS_1_235"
    MTS_933_IRIS_TC_LOOP_IMPERIAL_BEACH_COUNTERCLOCK = "MTS_1_933"
    MTS_88_OLD_TOWN_FASHION_VALLEY = "MTS_1_88"
    OTHER = 98
    # Many more to be added here, ask ETC


class ModeDecision(IntEnum):
    """
    Integer mapping for decisions to choose a commute mode
    """
    LOWEST_COST = 1
    SHORTEST_DOOR_TO_DOOR_TRAVEL_TIME = 2
    SMALLEST_CHANCE_FOR_DELAYS = 3
    MOST_COMFORTABLE = 4
    LEAST_WALKING = 5
    DEPENDS_ON_TIME_OF_DAY = 6
    DEPENDS_ON_TRAVEL_PARTY = 7
    DEPENDS_ON_WHO_PAYS = 8
    OTHER_SPECIFY = 98


class ActivityType(IntEnum):
    """
    Integer mapping for activity types

    """
    USUAL_WORKPLACE = 1
    HOME = 2
    HOTEL = 3
    OTHER_BUSINESS = 4 
    OTHER_RESIDENCE = 5 
    OTHER = 6 


class ParkingLocation(IntEnum):
    """
    Integer Mapping for Airport parking locations
    """
    TERM1_PARKING_PLAZA = 1
    TERM2_PARKING_PLAZA = 2
    TERM1_CURBSIDE_VALET = 3
    TERM2_CURBSIDE_VALET = 4
    OFF_AIRPORT_PARKING = 5
    EMPLOYEE_LOT_3665_ADMIRAL_BOLAND_WAY = 6
    ADMIN_BUILDING_LOT_2417_MCCAIN_ROAD = 7
    OTHER = 98
    REFUSED = 99

class ParkingCostFrequency(IntEnum):
    """
    Integer mapping for parking cost frequencies
    """
    TOTAL = 1
    MONTHLY = 2
    DAILY = 3
    HOURLY = 4
    OTHER_SEPCIFY = 98
    REFUSED = 99


class ParkingReimbursement(IntEnum):
    """
    Integer mapping for Parking Reimbursement Status
    """
    REIMBURSED_EMPLOYER_CLIENT = 1
    REIMBURSED_OTHER_THIRD_PARTY = 2
    NOT_REIMBURSED = 3
    DONT_KNOW = 4


class CarAvailability(IntEnum):
    """
    Integer mapping for car availability
    """

    CAR_AVAILABLE = 1
    DONT_HAVE_CAR = 2
    CAR_UNAVAILABLE = 3
    DONT_DRIVE = 4
    OTHER = 98
    REFUSED = 99


class SanFlightFrequency(IntEnum):
    """
    Integer mapping for flight frequency
    """
    ONCE_OR_TWICE_PER_YEAR = 1
    THREE_TO_FIVE_PER_YEAR = 2
    SIX_TO_TEN_PER_YEAR = 3
    ELEVEN_TO_TWENTY_PER_YEAR = 4
    TWENTY_ONE_OR_MORE_PER_YEAR = 5
    NEVER = 6
    ALWAYS = 7 #only relevant for access mode use


class ReasonsNoTransit(IntEnum):
    """
    Integer mapping for reasons of not choosing transit
    """
    NOT_CONVENIENT = 1
    DISLIKE_CROWDED_TRAINS_BUSES = 2
    NOT_FLEXIBLE = 3
    NOT_RELIABLE = 4
    NOT_SAFE = 5
    TAKES_TOO_LONG = 6
    NOT_ECONOMICAL = 7
    DONT_KNOW_HOW = 8
    TOO_MUCH_WALKING_STAIRS = 9
    NO_GOOD_OPTIONS = 10
    DISLIKE_PUBLIC_TRANSPORT = 11
    DISLIKE_PUBLIC_TRANSPORT_WITH_LUGGAGE = 12
    OTHER_SPECIFY = 98


class TransitUseFrequency(IntEnum):
    """
    Integer mapping for weekly transit use frequency
    """
    NONE = 0
    ONE_DAY = 1
    TWO_DAYS = 2
    THREE_DAYS = 3
    FOUR_DAYS = 4
    FIVE_DAYS = 5
    SIX_DAYS = 6
    SEVEN_DAYS = 7

class OtherTransitUseFrequency(IntEnum):
    """
    Integer Mapping for other aiport's transit use frequency
    """
    ONE_TIME = 1
    TWO_TIMES = 2
    THREE_TIMES = 3
    FOUR_TIMES = 4
    MORE_THAN_FIVE_TIMES = 5
    NEVER = 6
    OTHER = 98
    REFUSED = 99


class Age(IntEnum):
    """
    Integer mapping for age categories
    """

    AGE_18_19 = 1
    AGE_20_24 = 2
    AGE_25_29 = 3
    AGE_30_34 = 4
    AGE_35_39 = 5
    AGE_40_44 = 6
    AGE_45_49 = 7
    AGE_50_54 = 8
    AGE_55_59 = 9
    AGE_60_64 = 10
    AGE_65_74 = 11
    AGE_75_OR_MORE = 12
    PREFER_NOT_TO_SAY = 13
    OTHER = 98
    REFUSED = 99



class Gender(IntEnum):
    """
    Integer mapping for gender
    """
    MALE = 1
    FEMALE = 2
    TRANSGENDER = 3
    NON_BINARY_THIRD_GENDER = 4
    PREFER_NOT_TO_SAY = 5
    OTHER_SPECIFY = 98
    REFUSED = 99



class HouseholdSize(IntEnum):
    """
    Integer mapping for number of persons in household
    """

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN_OR_MORE = 10
    OTHER = 98
    REFUSED = 99


class HouseholdVehicles(IntEnum):
    """
    Integer mapping for number of vehicles in household
    """

    NONE = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT_OR_MORE = 8
    OTHER = 98
    REFUSED = 99


class HouseholdIncome(IntEnum):
    """
    Integer mapping for household income ranges
    """

    LESS_THAN_15K = 1
    BETWEEN_15K_20K = 2
    BETWEEN_20K_25K = 3
    BETWEEN_25K_30K = 4
    BETWEEN_30K_35K = 5
    BETWEEN_35K_40K = 6
    BETWEEN_40K_45K = 7
    BETWEEN_45K_50K = 8
    BETWEEN_50K_60K = 9
    BETWEEN_60K_75K = 10
    BETWEEN_75K_100K = 11
    BETWEEN_100K_150K = 12
    ABOVE_150K = 13
    PREFER_NOT_TO_SAY = 14  
    OTHER = 98
    REFUSED = 99


class HouseholdWorkers(IntEnum):
    """
    Integer mapping for number of workers in household
    """

    NONE = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN_OR_MORE = 10
    OTHER = 98
    REFUSED = 99


class NumTransfers(IntEnum): 
    """
    Integer mapping for number of transfers
    """
    NONE = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR_OR_MORE = 4 
    OTHER = 98
    REFUSED = 99

class SurveyLanguage(Enum):
    """
    Mapping for Survey Language
    """
    ENGLISH = "ENGLISH"
    SPANISH = "SPANI"
    OTHER = 98
    REFUSED = 99