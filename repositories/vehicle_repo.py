"""
Filename: vehicle_repo.py
Author: Juan Estrada
Date: 2024-09-16
Description: VehicleRepository that handles interactions with the database
"""

import os

from bson import ObjectId
from pymongo import MongoClient
from pymongo.response import Response
from flask import Response, json

from DataSetReader import dataset_reader, add_vehicles_array
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
            vehicle_id = ObjectId(veh_id)
            vehicle = self.collection.find_one({"_id": vehicle_id})
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

            vehicle_id = ObjectId(veh_id)
            updated_body = {
                "$set": {"make": updated_data['make'], "model": updated_data['model']}
            }
            updated_vehicle = self.collection.update_one({"_id": vehicle_id}, updated_body)

            if updated_vehicle.modified_count > 0:
                return Response(response=json.dumps({"message": "Vehicle updated successfully"}), status=200,
                                mimetype='application/json')
            return Response(response=json.dumps({"message": "Vehicle couldn't be updated"}), status=404,
                            mimetype='application/json')
        except Exception as ex:
            return Response(response=json.dumps({"message": f"Error updating data: {str(ex)}"}),
                            status=500, mimetype='application/json')

    def delete_vehicle(self, veh_id):
        """ Repository method that handles deleting a vehicle from the database """
        try:
            vehicle_id = ObjectId(veh_id)

            deleted_vehicle = self.collection.delete_one({"_id": vehicle_id})
            if deleted_vehicle.deleted_count > 0:
                return Response(response=json.dumps({"message": "Vehicle deleted successfully"}), status=200,
                                mimetype='application/json')
            return Response(response=json.dumps({"message": "Vehicle couldn't be deleted"}), status=404,
                            mimetype='application/json')
        except Exception as ex:
            return Response(response=json.dumps({"message": f"Error Deleting data: {str(ex)}"}),
                            status=500, mimetype='application/json')

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


