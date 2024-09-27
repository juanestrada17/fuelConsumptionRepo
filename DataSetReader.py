"""
Filename: DataSetReader.py
Author: Juan Estrada
Date: 2024-09-16
Description: Reads the csv file and returns an array of vehicle objects
"""
import os
import pandas as pd
from pymongo import MongoClient
from models.Vehicle import Vehicle
from dotenv import load_dotenv

try:
    load_dotenv()
    mongo_uri = os.getenv('MONGO_URI')
    db_name = os.getenv('MONGO_DB_NAME')
    collection_name = os.getenv('MONGO_COLLECTION_NAME')

    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
except Exception as ex:
    print(f"Error connection to the database: {ex}")


def dataset_reader(file_path):
    """Takes a file path as an argument and adds each record to an array of vehicles"""
    vehicles = []
    try:
        df = pd.read_csv(file_path, encoding='latin-1')
        for _, row in df.iterrows():
            model_year = row['Model year']
            make = row['Make']
            model = row['Model']
            vehicle_class = row['Vehicle class']
            engine_size = row['Engine size (L)']
            cylinder = row['Cylinders']
            transmission = row['Transmission']
            fuel_type = row['Fuel type']
            city_l_100km = row['City (L/100 km)']
            highway_l_100km = row['Highway (L/100 km)']
            combined_l_100km = row['Combined (L/100 km)']
            combined_mpg = row['Combined (mpg)']
            co2_emission = row['CO2 emissions (g/km)']
            co2_rating = row['CO2 rating']
            smog_rating = row['Smog rating']
            vehicle = Vehicle(model_year, make, model, vehicle_class, engine_size, cylinder, transmission, fuel_type,
                              city_l_100km, highway_l_100km, combined_l_100km, combined_mpg, co2_emission, co2_rating,
                              smog_rating)
            vehicles.append(vehicle)
    except FileNotFoundError:
        print("File could not be found")
    except UnicodeDecodeError:
        print("There was an error reading from the file")
    return vehicles


def display_vehicles(vehicles):
    """Takes an array of vehicles and displays information about their fuel consumption ratings"""
    print("Full Name: Juan Estrada")
    for vehicle in vehicles:
        print(vehicle)


def add_vehicles_array(vehicles):
    """ Creates an array of vehicle dictionaries and returns only the first 100 records added to it"""
    vehicles_array = []
    for vehicle in vehicles:
        vehicles_array.append(vehicle.vehicle_to_dic())
    return vehicles_array[:100]


def seed_database():
    """ Inserts an array of dictionaries made from the fuel consumption ratings
    dataset into the specified collection """
    try:
        dataset = 'my2024-fuel-consumption-ratings.csv'
        vehicles = dataset_reader(dataset)
        vehicles_arr = add_vehicles_array(vehicles)
        collection.insert_many(vehicles_arr)
    except Exception as e:
        print(f"Error seeding the database {e}")
