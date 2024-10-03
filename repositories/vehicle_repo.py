"""
Filename: vehicle_repo.py
Author: Juan Estrada
Date: 2024-09-16
Description: VehicleRepository that handles interactions with the database
Modified date: 2024-09-29
"""
import io
import os
from collections import Counter

import pandas as pd
from pymongo import MongoClient
from pymongo.response import Response
from flask import Response, json
import matplotlib.pyplot as plot
from DataSetReader import dataset_reader, add_vehicles_array, create_csv_from_array
from models.Vehicle import Vehicle
from dotenv import load_dotenv


class VehicleRepository:
    """ VehicleRepository that handles interactions with the database """

    def __init__(self):

        load_dotenv()
        mongo_uri = os.getenv('MONGO_URI')
        db_name = os.getenv('MONGO_DB_NAME')
        collection_name = os.getenv('MONGO_COLLECTION_NAME')

        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_vehicle(self, vehicle):
        """ Repository method that handles inserting a vehicle to the database """
        try:
            self.collection.insert_one(vehicle.vehicle_to_dic())

            response = Response(response=json.dumps({"message": "Vehicle added successfully"}), status=200,
                                mimetype='application/json')

            return response
        except Exception as ex:
            return Response(response=json.dumps({"message": f"Error inserting data: {str(ex)}"}),
                            status=500, mimetype='application/json')

    def insert_many_vehicles(self, vehicles):
        """ Repository method that handles inserting many vehicles to the database """
        try:
            self.collection.insert_many(vehicles)
            return Response(response=json.dumps({"message": "Vehicles added successfully"}), status=200,
                            mimetype='application/json')
        except Exception as ex:
            return Response(response=json.dumps({"message": f"Error inserting data: {str(ex)}"}),
                            status=500, mimetype='application/json')

    def get_vehicle(self, veh_id):
        """ Repository method that handles getting a vehicle from the database """
        try:
            vehicle = self.collection.find_one({"_id": veh_id})
            return Vehicle.vehicle_from_dict(vehicle) if vehicle else None
        except Exception as ex:
            return Response(response=json.dumps({"message": f"Error getting data: {str(ex)}"}),
                            status=500, mimetype='application/json')

    def get_all_vehicles(self):
        """ Repository method that handles getting all vehicles from the database """
        try:
            vehicles = list(self.collection.find())

            for vehicle in vehicles:
                vehicle["_id"] = str(vehicle["_id"])

            # return json.dumps(vehicles)
            return [Vehicle.vehicle_from_dict(vehicle) for vehicle in vehicles]
        except Exception as ex:
            return Response(response=json.dumps({"message": f"Error inserting data: {str(ex)}"}),
                            status=500, mimetype='application/json')

    def update_vehicle(self, veh_id, updated_data):
        """ Repository method that handles updating a vehicle from the database """
        try:

            updated_body = {
                "$set": {"make": updated_data['make'], "model": updated_data['model']}
            }
            updated_vehicle = self.collection.update_one({"_id": veh_id}, updated_body)

            if updated_vehicle.modified_count > 0:
                return Response(response=json.dumps({"message": "Vehicle updated successfully"}), status=200,
                                mimetype='application/json')
            return Response(response=json.dumps({"message": "Vehicle not found"}), status=404,
                            mimetype='application/json')
        except Exception as ex:
            return Response(response=json.dumps({"message": f"Error updating data: {str(ex)}"}),
                            status=500, mimetype='application/json')

    def delete_vehicle(self, veh_id):
        """ Repository method that handles deleting a vehicle from the database """
        try:

            deleted_vehicle = self.collection.delete_one({"_id": veh_id})
            if deleted_vehicle.deleted_count > 0:
                return Response(response=json.dumps({"message": "Vehicle deleted successfully"}), status=200,
                                mimetype='application/json')
            return Response(response=json.dumps({"message": "Vehicle couldn't be deleted"}), status=404,
                            mimetype='application/json')
        except Exception as ex:
            return Response(response=json.dumps({"message": f"Error Deleting data: {str(ex)}"}),
                            status=500, mimetype='application/json')

    def create_csv(self):
        """ Repository method that handles creating a csv file from data"""
        vehicles = list(self.collection.find())
        create_csv_from_array(vehicles)

    def seed_database(self):
        """ Repository method that handles seeding the database using the dataset """
        try:
            dataset = 'my2024-fuel-consumption-ratings.csv'
            vehicles = dataset_reader(dataset)
            vehicles_arr = add_vehicles_array(vehicles)
            self.collection.delete_many({})
            self.collection.insert_many(vehicles_arr)
        except Exception as e:
            print(f"Error seeding the database {e}")

    def generate_chart(self, column):
        """ Takes a column as an argument and generates a bar chart, pie chart, scatter plot or histogram.
            Transforms the graph into an in-memory image and returns it as part of the response.

            Args:
                column (str): The column or columns passed to generate the chart.

            Returns:
                A response with a generated chart as an image
            """
        try:
            vehicles = list(self.collection.find())
            vehiclesDf = pd.DataFrame(vehicles)
            plot.figure(figsize=(8, 6))

            match column:
                case 'make_mpg':
                    plot.title('Combined mpg per make')
                    average_mpg = vehiclesDf.groupby('make')['combined_mpg'].mean(numeric_only=True).reset_index()
                    plot.bar(average_mpg['make'], average_mpg['combined_mpg'], color=['green', 'tab:blue', 'tab:red',
                                                                                      'tab:orange', 'tab:purple'])
                    plot.xlabel('Make')
                    plot.ylabel('Average MPG')
                case 'engine_mpg':
                    plot.title('Combined mpg and engine size scatter plot')
                    engine_size = [str(vehicle['engine_size']) for vehicle in vehicles]
                    combined_mpg = [str(vehicle['combined_mpg']) for vehicle in vehicles]
                    plot.scatter(engine_size, combined_mpg, color='green', marker='o')
                    plot.xlabel('Engine-size')
                    plot.ylabel('Combined MPG')
                case 'co2_emission':
                    plot.title('Co2 emission histogram')
                    co2_emission = [str(vehicle['co2_emission']) for vehicle in vehicles]
                    plot.hist(co2_emission, bins=6, color='green')
                    plot.xticks(rotation=90)
                    plot.xlabel('Co2 emission')
                    plot.ylabel('Frequency')
                case 'transmission':
                    plot.title('Transmission % pie chart')
                    transmission = [str(vehicle['transmission']) for vehicle in vehicles]
                    trans_count = Counter(transmission)
                    total_trans = sum(trans_count.values())
                    trans_percent = [percent / total_trans * 100 for percent in trans_count.values()]
                    trans_keys = list(trans_count.keys())

                    plot.pie(trans_percent, labels=trans_keys, autopct='%1.1f%%')
                case 'fuel_mpg':
                    plot.title('Combined mpg per fuel type')
                    average_mpg = vehiclesDf.groupby('fuel_type')['combined_mpg'].mean().reset_index()
                    plot.bar(average_mpg['fuel_type'], average_mpg['combined_mpg'], color='green')
                    plot.xlabel('Fuel type')
                    plot.ylabel('Average MPG')
                case 'consumption':
                    plot.title('Fuel consumption per make')

                    consumption = {
                        'make' : [str(vehicle['make']) for vehicle in vehicles],
                        'city_l_100km' : [vehicle['city_l_100km'] for vehicle in vehicles],
                        'highway_l_100km' : [vehicle['highway_l_100km'] for vehicle in vehicles],
                        'combined_l_100km' : [vehicle['combined_l_100km'] for vehicle in vehicles],
                    }
                    df = pd.DataFrame(consumption)

                    average_fuel_consumption = df.groupby('make').mean()
                    average_fuel_consumption.plot(kind='bar', figsize=(16, 12), color=['green', 'tab:red', 'tab:blue'])
                    plot.xlabel('Make')
                    plot.ylabel('Average Fuel Consumption')
                case _:
                    return

            # in memory binary img
            graphImage = io.BytesIO()
            plot.savefig(graphImage, format='png')
            # start of stream
            graphImage.seek(0)
            plot.close()
            return Response(graphImage, mimetype='image/png')
        except Exception as ex:
            return Response(response=json.dumps({"message": f"Error graph data: {str(ex)}"}),
                            status=500, mimetype='application/json')



