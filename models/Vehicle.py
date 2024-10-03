"""
Filename: Vehicle.py
Author: Juan Estrada
Date: 2024-09-16
Description: Contains the Vehicle class and its attributes.
Modified date: 2024-09-29
"""


class Vehicle:
    """
    A class representing a vehicle

    Attributes:
        model_year(int): the year model of the vehicle
        make (str): the make of the car
        model (str): the model of the vehicle
        vehicle_class (str): the vehicle class
        engine_size (float): the engine size
        cylinder (int): the cylinder of the vehicle
        transmission (str): the transmission of the vehicle
        fuel_type (str): the fuel type of the vehicle
        city_l_100km (float): City fuel consumption rating shown in litres per 100 kilometres
        highway_l_100km (float): Highway fuel consumption rating shown in litres per 100 kilometres
        combined_l_100km (float): Combined fuel consumption rating shown in litres per 100 kilometres
        combined_mpg (int): The combined rating expressed in miles per imperial gallon
        co2_emission (int): The vehicle's tailpipe emissions of carbon dioxide shown in grams per kilometre
        for combined city and highway driving
        co2_rating (int): The vehicle's tailpipe emissions of carbon dioxide rated on a scale from 1
        (worst) to 10 (best)
        smog_rating (int): The vehicle's tailpipe emissions of smog-forming pollutants rated on a scale from 1 (worst)
         to 10 (best) n/a
         _id: id of the record stored in the database
    """

    def __init__(self, model_year: int, make: str, model: str, vehicle_class: str, engine_size: float,
                 cylinder: int, transmission: str, fuel_type: str, city_l_100km: float,
                 highway_l_100km: float, combined_l_100km: float, combined_mpg: int, co2_emission: int,
                 co2_rating: int, smog_rating: int, _id: str
                 ):
        """
        Initializes a vehicle object

        Parameters:
            model_year(int): the year model of the vehicle
            make (str): the make of the car
            model (str): the model of the vehicle
            vehicle_class (str): the vehicle class
            engine_size (float): the engine size
            cylinder (int): the cylinder of the vehicle
            transmission (str): the transmission of the vehicle
            fuel_type (str): the fuel type of the vehicle
            city_l_100km (float): City fuel consumption rating shown in litres per 100 kilometres
            highway_l_100km (float): Highway fuel consumption rating shown in litres per 100 kilometres
            combined_l_100km (float): Combined fuel consumption rating shown in litres per 100 kilometres
            combined_mpg (int): The combined rating expressed in miles per imperial gallon
            co2_emission (int): The vehicle's tailpipe emissions of carbon dioxide shown in grams per kilometre
            for combined city and highway driving
            co2_rating (int): The vehicle's tailpipe emissions of carbon dioxide rated on a scale from 1
            (worst) to 10 (best)
            smog_rating (int): The vehicle's tailpipe emissions of smog-forming pollutants rated on a scale from 1 (worst)
             to 10 (best) n/a
            _id: id of the record stored in the database

        """
        self._id = _id
        self.model_year = model_year
        self.make = make
        self.model = model
        self.vehicle_class = vehicle_class
        self.engine_size = engine_size
        self.cylinder = cylinder
        self.transmission = transmission
        self.fuel_type = fuel_type
        self.city_l_100km = city_l_100km
        self.highway_l_100km = highway_l_100km
        self.combined_l_100km = combined_l_100km
        self.combined_mpg = combined_mpg
        self.co2_emission = co2_emission
        self.co2_rating = co2_rating
        self.smog_rating = smog_rating

    def __str__(self):
        """
        Returns a string representation of the vehicle
        """
        return (f"Model Year: {self.model_year}, Make: {self.make}, Model: {self.model}, "
                f"Vehicle Class: {self.vehicle_class}, Engine: {self.engine_size}, "
                f"Cylinder: {self.cylinder}, Transmission: {self.transmission}, Fuel: {self.fuel_type}"
                f"city_l_100km: {self.city_l_100km}, highway_l_100km: {self.highway_l_100km},"
                f"combined_l_100km: {self.combined_l_100km}, combined_mpg: {self.combined_mpg}, Co2 Emission:"
                f"{self.co2_emission}, Co2 Rating: {self.co2_rating}, Smog Rating : {self.smog_rating}")

    # Makes object data a dictionary
    def vehicle_to_dic(self):
        """ Transforms a vehicle to a dictionary """
        return {
            "_id": self._id,
            'model_year': self.model_year,
            'make': self.make,
            'model': self.model,
            'vehicle_class': self.vehicle_class,
            'engine_size': self.engine_size,
            'cylinder': self.cylinder,
            'transmission': self.transmission,
            'fuel_type': self.fuel_type,
            'city_l_100km': float(self.city_l_100km),
            'highway_l_100km': float(self.highway_l_100km),
            'combined_l_100km': float(self.combined_l_100km),
            'combined_mpg': float(self.combined_mpg),
            'co2_emission': float(self.co2_emission),
            'co2_rating': float(self.co2_rating),
            'smog_rating': float(self.smog_rating)
        }

    # transforms data received from dictionary into obj
    @staticmethod
    def vehicle_from_dict(data):
        """ Transforms a dictionary into a vehicle object """
        return Vehicle(_id=data.get('_id'), model_year=data['model_year'], make=data['make'], model=data['model'],
                       vehicle_class=data['vehicle_class'],
                       engine_size=data['engine_size'], cylinder=data['cylinder'], transmission=data['transmission'],
                       fuel_type=data['fuel_type'],
                       city_l_100km=data['city_l_100km'], highway_l_100km=data['highway_l_100km'],
                       combined_l_100km=data['combined_l_100km'],
                       combined_mpg=data['combined_mpg'], co2_emission=data['co2_emission'],
                       co2_rating=data['co2_rating'],
                       smog_rating=data['smog_rating'])
