"""
Filename: vehicle_controller.py
Author: Juan Estrada
Date: 2024-09-16
Description: VehicleController that handles interaction between views and services
"""

from services.vehicle_service import VehicleService


class VehicleController:
    """ VehicleController that handles interaction between views and services """
    def __init__(self):
        self.service = VehicleService()

    def insert_vehicle(self, model_year, make, model, vehicle_class, engine_size,
                       cylinder, transmission, fuel_type, city_l_100km,
                       highway_l_100km, combined_l_100km, combined_mpg, co2_emission,
                       co2_rating, smog_rating):
        """ Controller method that handles inserting a vehicle to the database """
        return self.service.insert_vehicle(model_year, make, model, vehicle_class, engine_size,
                                           cylinder, transmission, fuel_type, city_l_100km,
                                           highway_l_100km, combined_l_100km, combined_mpg, co2_emission,
                                           co2_rating, smog_rating)

    def insert_vehicles(self, vehicles):
        """ Controller method that handles inserting many vehicles to the database """
        return self.service.insert_vehicles(vehicles)

    def get_vehicle(self, veh_id):
        """ Controller method that handles getting a vehicle from the database """
        return self.service.get_vehicle(veh_id)

    def get_all_vehicles(self):
        """ Controller method that handles getting all vehicles from the database """
        return self.service.get_all_vehicles()

    def update_vehicle(self, veh_id, updated_data):
        """ Controller method that handles updating a vehicle from the database """
        return self.service.update_vehicle(veh_id, updated_data)

    def delete_vehicle(self, veh_id):
        """ Controller method that handles deleting a vehicle from the database """
        return self.service.delete_vehicle(veh_id)

    def seed_database(self):
        """ Controller method that handles seeding the database """
        return self.service.seed_database()
