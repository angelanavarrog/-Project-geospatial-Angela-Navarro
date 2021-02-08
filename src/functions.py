# Import all libraries that are used

from pymongo import MongoClient
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
import pandas as pd
from pandas import DataFrame
from dotenv import load_dotenv
import os
import requests
import json
from functools import reduce
import operator
import geopandas as gpd
import cartoframes
from cartoframes.viz import Map, Layer, popup_element


# Import our database from MongoClient where an .json file was used.

client = MongoClient()
db = client.companies
db

# Execution of first query to run filters based on number of employees.

filt1 = {"number_of_employees": {"$eq":90},"offices.city":{"$ne": "",}}
project1 = {"_id":0,"offices.city": 1,"number_of_employees": 1}
results1 = db.offices.find(filt1,project1).sort("number_of_employees",1)#.skip(1).limit(1)
results1

# Conversion of the obtained results in a pandas dataframe.
pd.DataFrame.from_dict(results1)

# Clean of the results apply a new filter based on the location of the office. NYC as was defined.

filt2 = {"number_of_employees": {"$eq":90},"offices.city": {'$eq': "New York"}}
project2 = {"_id":0,"name":1,"offices.city": 1,"number_of_employees": 1,"offices.latitude":1,"offices.longitude":1}
results2 = db.offices.find(filt2,project2).sort("number_of_employees",1)#.skip(1).limit(1)
results2

#  Conversion of results2 in a list and in a dataframe.

office_location = list(results2)
office_location

pd.DataFrame.from_dict(office_location)


# Definition of the coordinates of our office proposal and it conversion in a dataframe

office_lat = 40.7592189
office_long = -73.9783534

office_data = [("office","40.7592189","-73.9783534","POINT (-73.9783534 40.7592189)","office location")]
df_office = pd.DataFrame(office_data, columns = ["name","latitud","longitud","geometry","criteria"]) 
df_office

# By using folium, we define a map based on the given coordinates.

map_1 = folium.Map(location = [office_lat, office_long], zoom_start = 16)
map_1

# Once the first map has been defined, we define a function to stablish the exact location including a marker. We add it to the first map defined.

office_loc = folium.Marker(location = [office_lat, office_long], tooltip = "Office location proposal")
icono = Icon(color = "blue",
             prefix = "fa",
             icon = "building-o",
             icon_color = "black",
             tooltip = "Office location proposal")


# Establishment of our selected location on a map_1.

office_location = [office_lat, office_long]
marker_office = Marker(location = office_location, icon = icono)
marker_office.add_to(map_1)
map_1

# Load dotenv() to have tokens available to get info from the APIs. We ask for them.
load_dotenv()

tok1 = os.getenv("tok1")
tok2 = os.getenv("tok2")

# Now, we look for Starbucks information on the API by given the URL
url_query = 'https://api.foursquare.com/v2/venues/explore'
starbucks = "556f676fbd6a75a99038d8ec"

#

#

#