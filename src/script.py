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
print(db)

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

# Definition of a new variable that returns coordinates of the values in Data.

city = "New York"
def geocode(address):
    data = requests.get(f"https://geocode.xyz/{address}?json=1").json()
    try:
        return {
            "type":"Point",
            "coordinates":[float(data["longt"]),float(data["latt"])]}
    except:
        return data

donde = "New York"
data = requests.get(f"https://geocode.xyz/{donde}?json=1").json()


# Definition of a geocode variable.
nyc = geocode(city)
nyc = {'type': 'Point', 'coordinates': [40.7592189, -73.9783534]}


# Getting tokens
tok1 = os.getenv("tok1")
tok2 = os.getenv("tok2")

# Now, we look for Starbucks information on the API by the URL and by the venue.
url_query = 'https://api.foursquare.com/v2/venues/explore'
starbucks = "556f676fbd6a75a99038d8ec"

# Definition of parameters incuiding information in Starbucks query and stablishing a radius of 500m from the office.
parameters = {"client_id" : tok1,
              "client_secret" : tok2,
              "v": "20180323",
              "ll": f"{nyc.get('coordinates')[0]},{nyc.get('coordinates')[1]}",
              "query":f"Starbucks",
              "radius":500
}

# We request the information by joining the URL and the parameters
resp = requests.get(url= url_query, params = parameters)
data = json.loads(resp.text)

# Definition of variable by applying .get functions.

decoding_data = data.get("response")
decoded = decoding_data.get("groups")[0]
starbucks = decoded.get("items")

# We define a Starbucks map and its latitude and longitude.
map_starbucks = ["venue","name"]
m_latitude = ["venue","location","lat"]
m_longitude = ["venue","location","lng"]

# Definition of function that returns the items.

def getFromDict(diccionario,mapa):
    return reduce (operator.getitem,mapa,diccionario)

# Print values of results with index 0 to check we obtain the value "Starbucks".

print(getFromDict(starbucks[0],map_starbucks))

# Creation of a empty list and deefinitioon of a function that contains a dictionary on which we apply the .append function.

starbucks_nyc = []
for dic in starbucks:
    lis1 = {}
    lis1["name"] = getFromDict(dic,map_starbucks)
    lis1["latitud"] = getFromDict(dic,m_latitude)
    lis1["longitud"] = getFromDict(dic,m_longitude)
    starbucks_nyc.append(lis1)

# Conversion on a dataframe.

df_starbucks = pd.DataFrame(starbucks_nyc)
df_starbucks.head()

# Definition of a geodataframe to reflect the previous data frame on a cartoframe map.

gdf_starbucks = gpd.GeoDataFrame(df_starbucks, geometry = gpd.points_from_xy(df_starbucks.longitud,df_starbucks.latitud))
gdf_starbucks.head()

# Adding a new column defining the criteria

gdf_starbucks = gdf_starbucks.assign(name = [ "Starbucks"]*20,
               criteria = ["Starbucks"]*20)
gdf_starbucks.head()

# Relects it on a map

Map(Layer(gdf_starbucks, popup_hover = [popup_element("name","Starbucks in NYC")]))


# Now, we look for vegan restaurants information on the API by the URL and by the venue.

url2 = 'https://api.foursquare.com/v2/venues/explore'
vegan = "4bf58dd8d48988d1d3941735"

# Definition of parameters incuided  in vegan query and stablishing a radius of 500m from the office.

parametros_vegan = {"client_id" : tok1,
              "client_secret" : tok2,
              "v": "20180323",
              "ll": f"{nyc.get('coordinates')[0]},{nyc.get('coordinates')[1]}",
              "query":f"vegans",
                "radius":500
}


# We request the information by joining the URL and the parameters using .json function.

resp2 = requests.get(url = url_query, params = parametros_vegan)
data2 = json.loads(resp2.text)

# Definition of variable by applying .get functions.
decoding_data2 = data2.get("response")
decoded2 = decoding_data2.get("groups")[0]
vegan = decoded2.get("items")

# We define a vegan restaurants map and its latitude and longitude.

map_vegan = ["venue","name"]
m_latitudvegan = ["venue","location","lat"]
m_longitudvegan = ["venue","location","lng"]

# Definition of function that returns the items.

def getFromDict2(diccionario2,mapa2):
    return reduce (operator.getitem,mapa2,diccionario2)

# Print values of results with index 0 to check we obtain the values.

print(getFromDict2(vegan[0],map_vegan))

# Creation of a empty list and definition of a function that contains a dictionary on which we apply the .append function.

vegan_nyc = []
for dic in vegan:
    paralista2 = {}
    paralista2["name"] = getFromDict(dic,map_vegan)
    paralista2["latitud"] = getFromDict(dic,m_latitudvegan)
    paralista2["longitud"] = getFromDict(dic,m_longitudvegan)
    vegan_nyc.append(paralista2)


# Conversion on a dataframe.

df_vegans = pd.DataFrame(vegan_nyc)
df_vegans.head()


# Definition of a geodataframe to reflect the previous data frame on a cartoframe map.
gdf_vegan = gpd.GeoDataFrame(df_vegans, geometry = gpd.points_from_xy(df_vegans.longitud,df_vegans.latitud))
gdf_vegan.head()

# Adding a new column defining the criteria
gdf_vegan = gdf_vegan.assign(name = ["Beyond Sushi",
                                        "by CHLOE.",
                                        "Van Leeuwen Ice Cream",
                                        "Taco Dumbo",
                                        "L’Avenue",
                                        "Taco Dumbo",
                                        "Urbanspace W52",
                                        "The Halal Guys",
                                        "The Little Beet",
                                        "Lenwich by Lenny's",
                                        "Le Pain Quotidien",
                                        "Mysttik Masala",
                                        "Museum of Modern Art (MoMA)",
                                        "Fogo de Chão",
                                        "Aldo Sohm Wine Bar",
                                        "Gregorys Coffee",
                                        "Pret A Manger",
                                        "Devon & Blakely",
                                        "Fig & Olive",
                                        "The Modern",
                                        "Black Tap",
                                        "Simon Sips",
                                        "Barilla Restaurants",
                                        "Estiatorio Milos",
                                        "Le Pain Quotidien",
                                        "Cock & Bull British Pub and Eatery",
                                        "Europa Cafe",
                                        "Forty2West",
                                        "Butter Midtown",
                                        "Natureworks"],
                                criteria = ["vegan"]*30)
gdf_vegan.head()


# Relects it on a map
Map(Layer(gdf_vegan, popup_hover = [popup_element("name","Vegan restaurants in NYC")]))



# Now, we look for basketball stadiums information on the API by the URL and by the venue.
url3 = 'https://api.foursquare.com/v2/venues/explore'
basketball_stadium = "4bf58dd8d48988d18b941735"

# Definition of parameters incuided  in basketball stadium query and stablishing a radius of 1000m from the office.
parametros_basket = {"client_id" : tok1,
              "client_secret" : tok2,
              "v": "20180323",
              "ll": f"{nyc.get('coordinates')[0]},{nyc.get('coordinates')[1]}",
              "query":f"basket_stadium",
                "radius":1000
}

# We request the information by joining the URL and the parameters using .json function.
resp3 = requests.get(url = url_query, params = parametros_basket)
data3 = json.loads(resp3.text)

# Definition of variable by applying .get functions.
decoding_data3 = data3.get("response")
decoded3 = decoding_data3.get("groups")[0]
basket_stadium = decoded3.get("items")

# We define a basketball staium map and its latitude and longitude.

map_stadium = ["venue","name"]

m_latitud_stadium = ["venue","location","lat"]
m_longitud_stadium = ["venue","location","lng"]

# Definition of function that returns the items.
def getFromDict3(diccionario3,mapa3):
    return reduce (operator.getitem,mapa3,diccionario3)

# Print values of results with index 0 to check we obtain the values.

print(getFromDict3(basket_stadium[0],map_stadium))

# Creation of a empty list and definition of a function that contains a dictionary on which we apply the .append function.

basket_stadium_nyc = []
for dic in basket_stadium:
    paralista3 = {}
    paralista3["name"] = getFromDict(dic,map_stadium)
    paralista3["latitud"] = getFromDict(dic,m_latitud_stadium)
    paralista3["longitud"] = getFromDict(dic,m_longitud_stadium)
    basket_stadium_nyc.append(paralista3)

# Conversion on a dataframe.
basket_stadium_nyc[0]
df_stadium = pd.DataFrame(basket_stadium_nyc)
df_stadium.head()

# Definition of a geodataframe to reflect the previous data frame on a cartoframe map.

gdf_stadiums = gpd.GeoDataFrame(df_stadium, geometry = gpd.points_from_xy(df_stadium.longitud,df_stadium.latitud))
gdf_stadiums

# Adding a new column defining the criteria

gdf_stadiums = gdf_stadiums.assign(name = [ "Regal E-Walk 4DX & RPX",
                           "Zaro's Bakery",
                           "Boomer Esiason's Stadium Grill",
                           "Stadium Grill At Bowlmor Lanes"],
               criteria = ["basketball stadium","basketball stadium","basketball stadium","basketball stadium"])
gdf_stadiums.head()


# Relects it on a map
Map(Layer(gdf_stadiums, popup_hover = [popup_element("name","Basketball Stadium")]))


# Now, we look for night clubs information on the API by the URL and by the venue.
url4 = 'https://api.foursquare.com/v2/venues/explore'
night_clubs = "4bf58dd8d48988d11f941735"

# Definition of parameters incuided  in night_clubs query and stablishing a radius of 1000m from the office.

parametros_night_clubs = {"client_id" : tok1,
              "client_secret" : tok2,
              "v": "20180323",
              "ll": f"{nyc.get('coordinates')[0]},{nyc.get('coordinates')[1]}",
              "query":f"night_clubs","radius":1000
}

# We request the information by joining the URL and the parameters using .json function.
resp4 = requests.get(url = url_query, params = parametros_night_clubs)
data4 = json.loads(resp4.text)

# Definition of variable by applying .get functions.
decoding_data4 = data4.get("response")
decoded4 = decoding_data4.get("groups")[0]
night_clubs = decoded4.get("items")

# We define a night clubs  map and its latitude and longitude.
map_night_clubs = ["venue","name"]
m_latitud_nightclubs = ["venue","location","lat"]
m_longitud_nightclubs = ["venue","location","lng"]

# Definition of function that returns the items.
def getFromDict4(diccionario4,mapa4):
    return reduce (operator.getitem,mapa4,diccionario4)

# Print values of results with index 0 to check we obtain the values.
print(getFromDict4(night_clubs[0],map_night_clubs))

# Creation of a empty list and definition of a function that contains a dictionary on which we apply the .append function.
night_clubs_nyc = []
for dic in night_clubs:
    paralista4 = {}
    paralista4["name"] = getFromDict(dic,map_night_clubs)
    paralista4["latitud"] = getFromDict(dic,m_latitud_nightclubs)
    paralista4["longitud"] = getFromDict(dic,m_longitud_nightclubs)
    night_clubs_nyc.append(paralista4)

# Conversion on a dataframe.
night_clubs_nyc[0]
df_night_clubs = pd.DataFrame(night_clubs_nyc)
df_night_clubs.head()

# Definition of a geodataframe to reflect the previous data frame on a cartoframe map.
gdf_night_clubs = gpd.GeoDataFrame(df_night_clubs, geometry = gpd.points_from_xy(df_night_clubs.longitud,df_night_clubs.latitud))
gdf_night_clubs.head()

# Adding a new column defining the criteria "night_clubs".
gdf_night_clubs = gdf_night_clubs.assign(name = ["Lavo",
                                        "Studio 54",
                                        "JOE & THE JUICE",
                                        "Tao",
                                        "STK Steakhouse Midtown NYC",
                                        "The Smith",
                                        "The View Restaurant & Lounge",
                                        "Chivas 1801 Club- NYC",
                                        "Flowers by Richard",
                                        "The Mean Fiddler",
                                        "Public House"],
                    criteria = ["night_clubs"]*11)
gdf_night_clubs.head()

# Relects it on a map

Map(Layer(gdf_night_clubs, popup_hover = [popup_element("name","Night clubs")]))


# Now, we look for transport options information on the API by the URL and by the venue.
url5 = 'https://api.foursquare.com/v2/venues/explore'
travel_transport = "4d4b7105d754a06379d81259"

# Definition of parameters incuided in travel query and stablishing a radius of 1000m from the office.
parametros_travel = {"client_id" : tok1,
              "client_secret" : tok2,
              "v": "20180323",
              "ll": f"{nyc.get('coordinates')[0]},{nyc.get('coordinates')[1]}",
              "query":f"travel_transport",
                ## "radius":1000
                    }

# We request the information by joining the URL and the parameters using .json function.

resp5 = requests.get(url = url_query, params = parametros_travel)
data5 = json.loads(resp5.text)

# Definition of variable by applying .get functions.

decoding_data5 = data5.get("response")
decoded5 = decoding_data5.get("groups")[0]
transport = decoded5.get("items")

# We define a transport points  map and its latitude and longitude.

map_transport = ["venue","name"]
m_latitud_transport = ["venue","location","lat"]
m_longitud_transport = ["venue","location","lng"]

# Definition of function that returns the items.
def getFromDict5(diccionario5,mapa5):
    return reduce (operator.getitem,mapa5,diccionario5)


# Print values of results with index 0 to check we obtain the values.
print(getFromDict5(transport[0],map_transport))


# Creation of a empty list and definition of a function that contains a dictionary on which we apply the .append function.
transport_nyc = []
for dic in transport:
    paralista5 = {}
    paralista5["name"] = getFromDict(dic,map_stadium)
    paralista5["latitud"] = getFromDict(dic,m_latitud_stadium)
    paralista5["longitud"] = getFromDict(dic,m_longitud_stadium)
    transport_nyc.append(paralista5)


# Conversion on a dataframe.
df_transports = pd.DataFrame(transport_nyc)
df_transports.head()

# Definition of a geodataframe to reflect the previous data frame on a cartoframe map.
gdf_transports = gpd.GeoDataFrame(df_transports, geometry = gpd.points_from_xy(df_transports.longitud,df_transports.latitud))
gdf_transports.head()

# Adding a new column defining the criteria "transports".
gdf_transports = gdf_transports.assign(name = [ "Theater Row - The Acorn",
                           "Solstice Travel Vacations",
                           "The Travel Inn",
                           "United Bus and Travel",
                           "Double Happiness Travel",
                           "K International Transport Co., Inc",
                           "Delgado Travel",
                           "Active Transport ServicesInc.",
                           "Rivas Travel & Multi Services"],
               criteria = ["transports"]*9)
gdf_transports.head()


# Relects it on a map
Map(Layer(gdf_transports, popup_hover = [popup_element("name","Transports")]))

# Finally, we concatenate our dataframes

df_criterias = pd.concat([df_office,gdf_starbucks, gdf_vegan,gdf_stadiums,gdf_night_clubs,gdf_transports])
df_criterias.head()
df_criterias = df_criterias

# Application of .unique to obtain values on criteria column.

df_criterias.criteria.unique()

# Definition of the final map

map_final = folium.Map (location = [40.7592189,-73.9783534],zoom_start = 15, min_lon = - 180, max_lon = 180, attr = 'Mapbox attribution')

# Function to establish different markers to each criteria.

for i,row in df_criterias.iterrows():
    name = {"location" : [row["latitud"],row["longitud"]],
            "tooltip" : row["name"]}
    
    if row["criteria"] == 'Starbucks':
        icon = Icon(color = "darkpurple",
                    prefix = "fa",
                    icon = "coffee",
                    icon_color = "beige")
    elif row["criteria"] == 'transports':
        icon = Icon(color = "blue",
                    prefix = "fa",
                    icon = "globe",
                    icon_color = "beige")
    elif row["criteria"] == 'office location':
        icon = Icon(color = "red",
                    prefix = "fa",
                    icon = "building-o",
                    icon_color = "beige")
    elif row["criteria"] == 'basketball stadium':
        icon = Icon(color = "orange",
                    prefix = "fa",
                    icon = "futbol-o",
                    icon_color = "beige")
    elif row["criteria"] == 'vegan':
        icon = Icon(color = "green",
                    prefix = "fa",
                    icon = "cutlery",
                    icon_color = "beige")
    else:
        icon = Icon(color = "white",
                    prefix = "fa",
                    icon = "glass",
                    icon_color = "lightblue")
        
    Marker(**name,icon = icon).add_to(map_final)

# Final map  
map_final