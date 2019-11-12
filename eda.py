from datetime import datetime
import prepare_data as prepdat
import settings as s

import seaborn as sns
import matplotlib
from matplotlib import pyplot as plt

raw_data = prepdat.get_data_from_pickle(s.path_data_folder + 'data_prepared.pkl')
data_pricing = prepdat.get_pricing_data(raw_data, s.path_input_folder)
data = prepdat.get_prices(data_pricing, s.path_input_folder)

plt.figure(figsize=(9, 8))
i = sns.distplot(data_prices['WEIGHT_OF_ITEMS'])
ii = i.get_figure()
ii.savefig("distribution_weight_of_items.png")

plt.figure(figsize=(9, 8))
i = sns.distplot(data_prices['BOOKING_DBD'])
ii = i.get_figure()
ii.savefig("distribution_booking_dbd.png")

plt.figure(figsize=(9, 8))
i = sns.distplot(data_prices['BOOKING_BAG_DBD'])
ii = i.get_figure()
ii.savefig("distribution_booking_bag_dbd.png")

plt.figure(figsize=(9, 8))
i = sns.distplot(data_prices['LENGTH_OF_STAY_INCL_FLIGHTTIME'])
ii = i.get_figure()
ii.savefig("distribution_length_of_stay_incl_flighttime.png")

plt.figure(figsize=(9, 8))
i = sns.distplot(data_prices['NBR_OF_PAX_IN_PNR'])
ii = i.get_figure()
ii.savefig("distribution_nbr_of_pax.png")

plt.figure(figsize=(9, 8))
i = sns.distplot(data_prices['BOOKING_TICKET_REVENUE_INCL_TAX'])
ii = i.get_figure()
ii.savefig("distribution_ticket_revenue.png")

plt.figure(figsize=(9, 8))
i = sns.distplot(data_prices['TOTAL_LEG_DISTANCE_KM'])
ii = i.get_figure()
ii.savefig("distribution_leg_distance_km.png")

plt.figure(figsize=(9, 8))
i = sns.countplot(data_prices['HUB_NL'])
ii = i.get_figure()
ii.savefig("count_hub_nl.png")

plt.figure(figsize=(9, 8))
i = sns.countplot(data_prices['DEPARTURE_AIRPORT'])
ii = i.get_figure()
ii.savefig("count_departure_airport.png")

plt.figure(figsize=(9, 8))
i = sns.countplot(data_prices['ARRIVAL_AIRPORT'])
ii = i.get_figure()
ii.savefig("count_arrival_airport.png")

plt.figure(figsize=(9, 8))
i = sns.countplot(data_prices['COUNTRY_CODE'])
ii = i.get_figure()
ii.savefig("count_country.png")

plt.figure(figsize=(9, 8))
i = sns.countplot(data_prices['DIRECTION'])
ii = i.get_figure()
ii.savefig("count_direction.png")

plt.figure(figsize=(9, 8))
i = sns.countplot(data_prices['WEEKDAY_OF_DEPARTURE'])
ii = i.get_figure()
ii.savefig("count_departure_weekday.png")

plt.figure(figsize=(9, 8))
i = sns.countplot(data_prices['MONTH_OF_DEPARTURE'])
ii = i.get_figure()
ii.savefig("count_departure_month.png")

plt.figure(figsize=(9, 8))
i = sns.countplot(data_prices['TIMESLOT_OF_DEPARTURE'])
ii = i.get_figure()
ii.savefig("count_departure_timeslot.png")

plt.figure(figsize=(9, 8))
i = sns.countplot(data_prices['WEEKDAY_OF_BOOKING'])
ii = i.get_figure()
ii.savefig("count_booking_weekday.png")

plt.figure(figsize=(9, 8))
i = sns.countplot(data_prices['WEEKDAY_OF_BOOKING_BAG'])
ii = i.get_figure()
ii.savefig("count_booking_bag_weekday.png")

plt.figure(figsize=(9, 8))
i = sns.countplot(data_prices['SEASONALITY'])
ii = i.get_figure()
ii.savefig("count_seasonality.png")

plt.figure(figsize=(9, 8))
i = sns.countplot(data_prices['SOURCE'])
ii = i.get_figure()
ii.savefig("count_source.png")

plt.figure(figsize=(9, 8))
i = sns.countplot(data_prices['GROUPBOOKING'])
ii = i.get_figure()
ii.savefig("count_groupbooking.png")





