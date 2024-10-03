"""
Filename: vehicle_service.py
Author: Juan Estrada
Date: 2024-09-16
Description: VehicleService that handles application's business logic
Modified date: 2024-09-29
"""

from repositories.vehicle_repo import VehicleRepository
from models.Vehicle import Vehicle


class VehicleService:
    """ Vehicle service that handles business logic"""
    def __init__(self):
        self.repository = VehicleRepository()

    def insert_vehicle(self, model_year, make, model, vehicle_class, engine_size,
                       cylinder, transmission, fuel_type, city_l_100km,
                       highway_l_100km, combined_l_100km, combined_mpg, co2_emission,
                       co2_rating, smog_rating, _id):
        """ Service method to insert a vehicle to the database """
        vehicle = Vehicle(model_year, make, model, vehicle_class, engine_size,
                          cylinder, transmission, fuel_type, city_l_100km,
                          highway_l_100km, combined_l_100km, combined_mpg, co2_emission,
                          co2_rating, smog_rating, _id)
        return self.repository.insert_vehicle(vehicle)

    def insert_vehicles(self, vehicles):
        """ Service method to insert multiple vehicles to the database """
        return self.repository.insert_many_vehicles(vehicles)

    def get_vehicle(self, veh_id):
        """ Service method to get a vehicle from the database """
        return self.repository.get_vehicle(veh_id)

    def get_all_vehicles(self):
        """ Service method to get all vehicles from the database """
        return self.repository.get_all_vehicles()

    def update_vehicle(self, veh_id, updated_data):
        """ Service method to update a vehicle from the database """
        return self.repository.update_vehicle(veh_id, updated_data)

    def delete_vehicle(self, veh_id):
        """ Service method to delete a vehicle from the database """
        return self.repository.delete_vehicle(veh_id)

    def create_csv(self):
        """ Service method that handles creating a csv file from data"""
        return self.repository.create_csv()

    def seed_database(self):
        """ Service method to seed the database with records """
        return self.repository.seed_database()

    def generate_chart(self, column):
        """ Service method that handles generating a chart """
        return self.repository.generate_chart(column)