# Import packages
import pandas as pd
from datetime import datetime, date

# Database imports
import pyodbc
import logging

# Custom imports
import settings as s
import credentials as c



def get_azure_data(query, database=None, authn='ActiveDirectoryPassword', dsn=None, dwh_username=None, dwh_password=None):
    """
    Retrieve data from the data warehouse.

    :param str query: Query to be executed.
    :param str database: (optional) Database from which the data should be retrieved.
    :param str authn: (optional) Type of authentication. Values:
        - ActiveDirectoryPassword: For Azure Active Directory username/password authentication to SQL Azure.
        - SqlPassword: For username/password authentication to SQL Server (Azure or otherwise).
        - DSN: For for Azure authentication via a DSN. If this value is chosen, the variable `dsn` is required.
    :param str dsn: (optional) Name of DSN used to make a connection. Is required if authn='DSN'.
    :param str dwh_username: (optional) DWH username used to make a connection. Is required if authn != 'DSN'.
    :param str dwh_password: (optional) DWH password used to make a connection. Is required if authn != 'DSN'.
    :return pandas.DataFrame: Data set.
    """

    # Connection settings for data warehouse
    if authn == 'DSN':
        connection_string = 'dsn='+dsn
    else:
        if s.local_production:
            driver = '{ODBC Driver 13 for SQL Server}'
        else:
            driver = '{ODBC Driver 17 for SQL Server}'
        server = 'tra-sqldwh-p.database.windows.net'
        connection_string = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+dwh_username+';PWD='+dwh_password+';Authentication='+authn

    connection = pyodbc.connect(connection_string)
    data = pd.read_sql(query, connection)
    return data


def get_data():
    """
    Retrieve leg data from database.

    :param datetime.date start_date: First date of booking data to retrieve.
    :param datetime.date end_date: Laste date of booking data to retrieve.
    :return pandas.DataFrame: Set with leg data.
    """

    query = """
set datefirst 1; -- Monday is first day of the week

DECLARE @StartDate Date;  
SET @StartDate = '2018-07-01';  

DECLARE @EndDate Date;  
SET @EndDate = '2019-06-30';  

WITH DIM_DATE AS
(
SELECT 
	[DATE_ID],
    [DAY] AS [DATE],
    [DAY_NUMBER_MONTH],
    [MONTH_NUMBER],
    [YEAR],
	CASE WHEN			CAST([DAY] as DATE)	BETWEEN '2018-04-27' AND '2018-05-03' 
				OR		CAST([DAY] as DATE)	BETWEEN '2018-07-06' AND '2018-08-19' 
				OR		CAST([DAY] as DATE)	BETWEEN '2018-10-12' AND '2018-10-23' 
				OR		CAST([DAY] as DATE)	BETWEEN '2018-12-20' AND '2018-12-30'
				OR		CAST([DAY] as DATE)	BETWEEN '2019-02-15' AND '2019-03-04'
				OR		CAST([DAY] as DATE)	BETWEEN '2019-04-19' AND '2019-04-28' 
				OR		CAST([DAY] as DATE)	BETWEEN '2019-07-05' AND '2019-08-18'
				THEN 'HIGH'
				ELSE 'LOW' 
				END AS [SEASONALITY_OUTBOUND],
	CASE WHEN			CAST([DAY] as DATE)	BETWEEN '2018-05-02' AND '2018-05-06' 
				OR		CAST([DAY] as DATE)	BETWEEN '2018-07-21' AND '2018-09-02'
				OR		CAST([DAY] as DATE)	BETWEEN '2018-10-18' AND '2018-10-28'
				OR		CAST([DAY] as DATE)	BETWEEN '2018-12-19' AND '2019-01-06'
				OR		CAST([DAY] as DATE)	BETWEEN '2019-02-22' AND '2019-03-10'
				OR		CAST([DAY] as DATE)	BETWEEN '2019-04-27' AND '2019-05-05'
				OR		CAST([DAY] as DATE)	BETWEEN '2019-07-20' AND '2019-09-01'
				THEN 'HIGH'
				ELSE 'LOW'
				END AS [SEASONALITY_INBOUND]
  FROM [DWH_COM].[VW_DIM_DATE]
  WHERE [DAY] BETWEEN @StartDate AND @EndDate
  )
, 



ANC_REV AS
(
SELECT
	AR.[SOURCE],
	AR.BKR_PLANNED_SEGMENT,
	AR.BKR_BOOKING,
	MAX(CAST(AR.CREATED_DATE as DATE))	AS [BOOK_DAY_BAG],
	SUM(ATY.[WEIGHT_OF_ITEMS])			AS [WEIGHT_OF_ITEMS],
	SUM(AR.[ANCILLARY_REVENUE])			AS [ANCILLARY_REVENUE]
FROM [DWH_COM].[VW_FCT_ANCILLARY_REVENUE] AS AR

RIGHT JOIN DWH_COM.[VW_DIM_ANCILLARY_TYPE] AS ATY			ON ATY.[BKR_ANCILLARY_TYPE] = AR.[BKR_ANCILLARY_TYPE] 
															AND ATY.[BL_CRUD] != 'D' 
															AND ATY.[BL_ISCURR] = 1 
															AND ATY.[SUBTYPE] = 'Baggage' 
															AND ATY.[WEIGHT_OF_ITEMS] > 0
WHERE	1=1 
		AND AR.[BL_CRUD] != 'D' 
		AND AR.[BL_ISCURR] = 1
		AND ATY.[DESCRIPTION] LIKE '5 B%'

GROUP BY 
	AR.[BKR_PLANNED_SEGMENT], 
	AR.[BKR_BOOKING], 
	AR.[SOURCE]
)
,



MASTER_QUERY AS
(
SELECT 
	BS.[BKR_PLANNED_SEGMENT],															/** set as index **/
	CAST(BO.[BOOKING_DATE] as DATE)						AS [BOOKING_DATE],
	BO.[BOOKING_DATE]									AS [BOOKING_DATETIME],
	BS.[DEPARTURE_AIRPORT],																/** check- to drop **/
	BS.[ARRIVAL_AIRPORT],																/** check- to drop **/
	AP.[COUNTRY_CODE],
	CASE	WHEN (BS.[DEPARTURE_AIRPORT] = 'AMS'	OR BS.[ARRIVAL_AIRPORT] = 'AMS')	THEN 'AMS'
			WHEN (BS.[DEPARTURE_AIRPORT] = 'EIN'	OR BS.[ARRIVAL_AIRPORT] = 'EIN')	THEN 'EIN'
			WHEN (BS.[DEPARTURE_AIRPORT] = 'RTM'	OR BS.[ARRIVAL_AIRPORT] = 'RTM')	THEN 'RTM'
			WHEN (BS.[DEPARTURE_AIRPORT] = 'GRQ'	OR BS.[ARRIVAL_AIRPORT] = 'GRQ')	THEN 'GRQ'
			ELSE 'NONE' 
			END AS [HUB_NL],
	PS.[DEPARTURE_DATETIME_PLS],														/** check- to drop **/
	CAST(PS.[DEPARTURE_DATETIME_PLS] AS DATE)			AS [DEPARTURE_DATE],			/** check- to drop **/
	PS.[ARRIVAL_DATETIME_PLS],															/** check- to drop **/
	CONVERT(varchar, PS.[ARRIVAL_DATETIME_PLS], 108)	AS [DEPARTURE_TIME],			/** check- to drop **/
	CAST(PS.[ARRIVAL_DATETIME_PLS] AS DATE)				AS [ARRIVAL_DATE],				/** check- to drop **/
	PS.[TOTAL_LEG_DISTANCE_KM],
	PS.[SEGMENT_DIRECTION]								AS [DIRECTION],
	BO.[NBR_OF_PAX_IN_PNR],
	BS.[TOTAL_TRIP_DURATION_IN_MIN]					AS [LENGTH_OF_STAY_INCL_FLIGHTTIME],
	AR.[SOURCE],											
	AR.[BOOK_DAY_BAG] AS [BOOKING_DATE_BAG],
	AR.[WEIGHT_OF_ITEMS],
	AR.[ANCILLARY_REVENUE],
	BO.[BKR_BOOKING],											/** check- to drop **/
	CASE	WHEN BS.[FARECLASSOFSERVICE] = 'W' THEN 'GROUP'
			ELSE 'SINGLE' 
			END AS [GROUPBOOKING],
	SUM(TR.[BASE_TICKET_REVENUE_INCL_TAX])				AS [BOOKING_TICKET_REVENUE_INCL_TAX]
FROM DWH_COM.[VW_DIM_BOOKED_SEGMENT] AS BS

LEFT JOIN DWH_COM.[VW_DIM_PLANNED_SEGMENT] AS PS	ON BS.[BKR_PLANNED_SEGMENT] = PS.[BKR_PLANNED_SEGMENT]	
													AND PS.[BL_CRUD] != 'D' 
													AND PS.[BL_ISCURR] = 1
LEFT JOIN DWH_COM.[VW_DIM_BOOKING] AS BO			ON BS.[BKR_BOOKING] = BO.[BKR_BOOKING]					
													AND BO.[BL_CRUD] != 'D' 
													AND BO.[BL_ISCURR] = 1
LEFT JOIN DWH_COM.[VW_FCT_TICKET_REVENUE] AS TR		ON (BS.[PASSENGERID] = TR.[PASSENGERID] 
													AND BS.[BKR_BOOKED_SEGMENT] = TR.[BKR_BOOKED_SEGMENT])	
													AND TR.[BL_CRUD] != 'D' 
													AND TR.[BL_ISCURR] = 1
LEFT JOIN ANC_REV AS AR								ON BS.[BKR_PLANNED_SEGMENT] = AR.[BKR_PLANNED_SEGMENT]	
													AND BS.[BKR_BOOKING] = AR.[BKR_BOOKING]	
LEFT JOIN [DWH_COM].[VW_DIM_AIRPORT] AS AP			ON BS.[ARRIVAL_AIRPORT] = AP.[IATA_CODE]					
													AND AP.[BL_CRUD] != 'D' 
													AND AP.[BL_ISCURR] = 1

WHERE	1=1
		AND BS.[BL_CRUD] != 'D' 
		AND BS.[BL_ISCURR] = 1
		AND BS.[OPERATING_AIRLINE] = 'HV'
		AND BS.[FIRMNESS] = 'E'
		AND CAST(PS.[DEPARTURE_DATETIME_PLS] as DATE) BETWEEN @StartDate AND @EndDate

GROUP BY 
	BS.[BKR_PLANNED_SEGMENT],
	BO.[BOOKING_DATE],
	BS.[DEPARTURE_AIRPORT],
	AP.[COUNTRY_CODE],
	BS.[ARRIVAL_AIRPORT],
	PS.[DEPARTURE_DATETIME_PLS],
	PS.[ARRIVAL_DATETIME_PLS],
	PS.[TOTAL_LEG_DISTANCE_KM],
	PS.[SEGMENT_DIRECTION],
	BO.[NBR_OF_PAX_IN_PNR],
	BS.[TOTAL_TRIP_DURATION_IN_MIN],
	BS.[XREF_AIRLINE_CODE],
	AR.[SOURCE],
	AR.[BOOK_DAY_BAG],
	AR.[WEIGHT_OF_ITEMS],
	AR.[ANCILLARY_REVENUE],
	BO.[BKR_BOOKING],
	BS.[FARECLASSOFSERVICE],
	BS.[FIRMNESS]
)


SELECT 
	[BKR_BOOKING],
	[DEPARTURE_AIRPORT],
	[ARRIVAL_AIRPORT],
	[HUB_NL],
	[COUNTRY_CODE],
	[DIRECTION],
	[TOTAL_LEG_DISTANCE_KM],
	DATEPART(weekday, [DEPARTURE_DATE])				AS [WEEKDAY_OF_DEPARTURE],
	DATEPART(Month, [DEPARTURE_DATE])				AS [MONTH_OF_DEPARTURE],
	CASE    WHEN [DEPARTURE_TIME]  BETWEEN '05:00:00' AND '08:00:00' THEN 'Morning Early'
			WHEN [DEPARTURE_TIME]  BETWEEN '08:00:00' AND '10:00:00' THEN 'Morning'
			WHEN [DEPARTURE_TIME]  BETWEEN '10:00:00' AND '12:00:00' THEN 'Morning Late'
			WHEN [DEPARTURE_TIME]  BETWEEN '12:00:00' AND '14:00:00' THEN 'Afternoon Early'
			WHEN [DEPARTURE_TIME]  BETWEEN '14:00:00' AND '16:00:00' THEN 'Afternoon'
			WHEN [DEPARTURE_TIME]  BETWEEN '16:00:00' AND '17:00:00' THEN 'Afternoon Late'
			WHEN [DEPARTURE_TIME]  BETWEEN '17:00:00' AND '19:00:00' THEN 'Evening'
			WHEN [DEPARTURE_TIME]  BETWEEN '19:00:00' AND '21:00:00' THEN 'Evening Late'
			ELSE 'Night' 
			END AS [TIMESLOT_OF_DEPARTURE],
	[BOOKING_DATE],
	DATEPART(weekday, [BOOKING_DATE])				AS [WEEKDAY_OF_BOOKING],
	DATEDIFF(DAY, [BOOKING_DATE], [DEPARTURE_DATE]) AS [BOOKING_DBD],
    [BOOKING_DATE_BAG],
	DATEPART(weekday, [BOOKING_DATE_BAG])				AS [WEEKDAY_OF_BOOKING_BAG],
	DATEDIFF(DAY, [BOOKING_DATE_BAG], [DEPARTURE_DATE]) AS [BOOKING_BAG_DBD],
	[LENGTH_OF_STAY_INCL_FLIGHTTIME],
	CASE	WHEN [DIRECTION] = 'I' THEN [SEASONALITY_INBOUND]
			ELSE [SEASONALITY_OUTBOUND]
			END AS [SEASONALITY],
	[SOURCE],
	[NBR_OF_PAX_IN_PNR],
	[BOOKING_TICKET_REVENUE_INCL_TAX],
	[GROUPBOOKING],
	CASE	WHEN [BOOKING_DATE_BAG] IS NULL 
										THEN CASE 
													 WHEN [BOOKING_DATE] >= '2019-03-04' THEN 1 
													 WHEN [BOOKING_DATE] >= '2018-07-18' THEN 2 
													 WHEN [BOOKING_DATE] >= '2018-07-12' THEN 3 
													 WHEN [BOOKING_DATE] >= '2018-03-30' THEN 4 
													 WHEN [BOOKING_DATE] >= '2017-12-18' THEN 5 
													 WHEN [BOOKING_DATE] >= '2017-09-20' THEN 6 
												END
			WHEN [BOOKING_DATE_BAG] IS NOT NULL 
										THEN CASE
													 WHEN [BOOKING_DATE_BAG] >= '2019-03-04' THEN 1 
													 WHEN [BOOKING_DATE_BAG] >= '2018-07-18' THEN 2 
													 WHEN [BOOKING_DATE_BAG] >= '2018-07-12' THEN 3 
													 WHEN [BOOKING_DATE_BAG] >= '2018-03-30' THEN 4 
													 WHEN [BOOKING_DATE_BAG] >= '2017-12-18' THEN 5 
													 WHEN [BOOKING_DATE_BAG] >= '2017-09-20' THEN 6 
												END
		ELSE 7
												END AS [PRICING_TIME],
	[WEIGHT_OF_ITEMS]
FROM MASTER_QUERY AS MQ
	
LEFT JOIN DIM_DATE ON [DATE] = [DEPARTURE_DATE]
WHERE 1=1
    
    """

    database = 'TRA-SQLDWH-P'
    data = get_azure_data(query=query, database=database, authn=s.dwh_authn, dwh_username=c.dwh_username, dwh_password=c.dwh_password)
    return data


def write_data_to_pickle(data, file_path):
    """
    Write data set to pickle. The resulting pickle will be saved in sub directory 'data'.

    :param pandas.DataFrame data: Data set to be saved as pickle.
    :param str file_path: Path to data set.
    """

    # Write data set to pickle
    if len(data) > 0:
        data.to_pickle(file_path)


def get_data_from_pickle(file_path):
    """
    Retrieve data from pickle. The resulting pickle will be obtained from sub directory 'data'.

    :param str file_path: Path to data set.
    :return pandas.DataFrame: Data set to be obtained from pickle
    """

    data = pd.read_pickle(file_path)
    return data

def get_pricing_data(data, path):
    """
    Retrieve data for pricing levels. The resulting levels are set in the SQL query manually based on when pricing specialists have decided on shifting levels up and down.

    :param pandas.DataFrame: Dataset.
    :param str path: path to local excel file for pricing level data.
    :return pandas.DataFrame: Dataset includig pricing levels
    """
    data_pricing = pd.read_excel(path + s.files['pricing_data'], decimal=',')

    data = pd.merge(data, data_pricing, how='left', on=['DEPARTURE_AIRPORT', 'ARRIVAL_AIRPORT', 'PRICING_TIME'])
    return data

def get_prices(data, path):
    """
    Retrieve data for prices linked to previously set levels. The resulting prices are set by pricing specialists.

    :param pandas.DataFrame: Dataset.
    :param str path: path to local excel file for pricing level data.
    :return pandas.DataFrame: Dataset includig prices
    """
    data_prices = pd.read_excel(path + s.files['prices_data'], decimal=',')

    data = pd.merge(data, data_prices, how='left', on=['LEVEL'])
    return data

def delete_columns(data, columns):
    """
    Delete columns that are not necessary for models (either because of GDPR or because they are only needed for unique values through SQL query)

    :param pandas.DataFrame: Dataset.
    :param list columns: List of column names which may be deleted
    :return pandas.DataFrame: Dataset needed for training models
    """
    for col in columns:
        data.drop(col, axis=1, inplace=True)
    return data


