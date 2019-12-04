# Import packages
from datetime import datetime
import seaborn as sns
import matplotlib
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib import pyplot as plt
import tikzplotlib
import pandas as pd

# Custom import
import prepare_data as prepdat
import settings as s

""""Retrieve heatmap correlation"""
# corr_matrix = data.corr()
# print(corr_matrix)
# corr_matrix.to_csv("corr_matrix.csv")
# print('pearson')
# print(data['PRICE_15KG'].head())
# print(data['PRICE_15KG'].corr(data['WEIGHT_OF_ITEMS']))
# print(data['PRICE_20KG'].corr(data['WEIGHT_OF_ITEMS']))
# print(data['PRICE_25KG'].corr(data['WEIGHT_OF_ITEMS']))
# print(data['PRICE_30KG'].corr(data['WEIGHT_OF_ITEMS']))
# print(data['PRICE_40KG'].corr(data['WEIGHT_OF_ITEMS']))
# print(data['PRICE_50KG'].corr(data['WEIGHT_OF_ITEMS']))
# print(data['GROUPBOOKING'].corr(data['WEIGHT_OF_ITEMS']))
# print(data['SEASONALITY'].corr(data['WEIGHT_OF_ITEMS']))
# print('pointbiserial')
# print(stats.pointbiserialr(data['GROUPBOOKING'], data['WEIGHT_OF_ITEMS']))
# print(stats.pointbiserialr(data['SEASONALITY'], data['WEIGHT_OF_ITEMS']))
"""End of heatmap correlation"""

    """""Start matplottikz"""
    #plt.figure(figsize=(9, 8))
    #plt.style.use("ggplot")
    #sns.distplot((data_prices['BOOKING_DBD']/1440))
    #plt.xlabel("days before departure")
    #tikzplotlib.save("mbd.tex", dpi=400)

    #plt.figure(figsize=(9, 8))
    #plt.style.use("ggplot")
    #sns.distplot(data_prices['WEIGHT_OF_ITEMS'])
    #plt.xlabel("paid luggage (in kg)")
    #tikzplotlib.save("pl.tex")

    #df100 = data_prices[data_prices['WEIGHT_OF_ITEMS'] < 100]
    #plt.figure(figsize=(9, 8))
    #plt.style.use("ggplot")
    #sns.distplot(df100['WEIGHT_OF_ITEMS'])
    #plt.xlabel("paid luggage (in kg)")
    #tikzplotlib.save("pl250.tex")

    #plt.figure(figsize=(9,8))
    #plt.style.use("ggplot")
    #plt.scatter(data_prices['TOTAL_LEG_DISTANCE_KM'][0:10000], data_prices['WEIGHT_OF_ITEMS'][0:10000])
    #plt.xlabel("total leg distance (in km)")
    #plt.ylabel("total mass of paid luggage (in kg)")
    #tikzplotlib.save("legdistance.tex")

    #data_prices['SEASONALITY'] = data_prices['SEASONALITY'].replace('1', 'high')
    #data_prices['SEASONALITY'] = data_prices['SEASONALITY'].replace('0', 'low')
    #plt.figure(figsize=(9, 8))
    #plt.style.use("ggplot")
    #sns.countplot(x='SEASONALITY', data=data_prices)
    #plt.ylabel("frequency")
    #plt.xlabel("")
    #tikzplotlib.save("season.tex")
#
    #data_prices['GROUPBOOKING'] = data_prices['GROUPBOOKING'].replace('1', 'group request')
    #data_prices['GROUPBOOKING'] = data_prices['GROUPBOOKING'].replace('0', 'individual booking')
#
    #plt.figure(figsize=(9, 8))
    #plt.style.use("ggplot")
    #sns.countplot(x='GROUPBOOKING', data=data_prices)
    #plt.ylabel("frequency")
    #plt.xlabel("")
    #tikzplotlib.save("group.tex")


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



# Get correlations for categorical variables
from scipy import stats
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
print('anovahub')
Fhub, rhub = stats.f_oneway(data_prices['WEIGHT_OF_ITEMS'], data_prices['HUB_NL'])
print(Fhub, rhub)
print('anovacountry')
data_prices['CC'] = le.fit_transform(data_prices['COUNTRY_CODE'])
Fcountry, rcountry = stats.f_oneway(data_prices['CC'], data_prices['WEIGHT_OF_ITEMS'])
print(Fcountry, rcountry)
print('anovaweekdaydep')
Fweekdep, rweekdep = stats.f_oneway(data_prices['WEEKDAY_OF_DEPARTURE'], data_prices['WEIGHT_OF_ITEMS'])
print(Fweekdep, rweekdep)
print('anovamonthdep')
Fmonthdep, rmonthdep = stats.f_oneway(data_prices['MONTH_OF_DEPARTURE'], data_prices['WEIGHT_OF_ITEMS'])
print(Fmonthdep, rmonthdep)
print('anovatimedep')
Ftimedep, rtimedep = stats.f_oneway(data_prices['TIMESLOT_OF_DEPARTURE'], data_prices['WEIGHT_OF_ITEMS'])
print(Ftimedep, rtimedep)
print('anovaweekdaybook')
Fbook, rbook = stats.f_oneway(data_prices['WEEKDAY_OF_BOOKING'], data_prices['WEIGHT_OF_ITEMS'])
print(Fbook, rbook)





