import pymongo
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


client = MongoClient()
db = client.companies

def location_suggestions(filt1, projects1,results1,office_location):
    ''' It takes the company information filtered by our defined criteria.
    It returns a Dataframe with company name and the office location (city, lat, long)'''

    filt1 = {"number_of_employees": {"$eq":90},"offices.city": {'$eq': "New York"}}
    project1 = {"_id":0,"name":1,"offices.city": 1,"number_of_employees": 1,"offices.latitude":1,"offices.longitude":1}
    results1 = db.offices.find(filt1,project1).sort("number_of_employees",1)
    office_location = list(results1)
    final_location = pd.DataFrame.from_dict(office_location)
    return final_location

def office_coordinates (office_data):
    ''' It takes the company company coooordinates and returns a Dataframe with company name, office location and criteria'''
    office_data = [("office","40.7592189","-73.9783534","POINT (-73.9783534 40.7592189)","office location")]
    df_office = pd.DataFrame(office_data, columns = ["name","latitud","longitud","geometry","criteria"]) 
    return df_office








