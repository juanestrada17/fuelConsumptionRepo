"""
Filename: vehicle_routes.py
Author: Juan Estrada
Date: 2024-09-16
Description: Defining the routes used in the application
"""

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from controllers.vehicle_controller import VehicleController

vehicle_blueprint = Blueprint("vehicle", __name__)
controller = VehicleController()


@vehicle_blueprint.route('/')
def index():
    """ Handles display and rendering of all vehicles from the database """
    vehicles = controller.get_all_vehicles()
    return render_template('index.html', vehicles=vehicles)


@vehicle_blueprint.route('/insert_form')
def insert_form():
    """ Handles rendering the insert form to the database """
    return render_template('add_vehicle.html')


@vehicle_blueprint.route('/insert_one', methods=['POST'])
def insert_vehicle():
    """ Handles inserting a record into the database by grabbing the form elements """
    model_year = request.form['model_year']
    make = request.form['make']
    model = request.form['model']
    vehicle_class = request.form['vehicle_class']
    engine_size = request.form['engine_size']
    cylinder = request.form['cylinder']
    transmission = request.form['transmission']
    fuel_type = request.form['fuel_type']
    city_l_100km = request.form['city_l_100km']
    highway_l_100km = request.form['highway_l_100km']
    combined_l_100km = request.form['combined_l_100km']
    combined_mpg = request.form['combined_mpg']
    co2_emission = request.form['co2_emission']
    co2_rating = request.form['co2_rating']
    smog_rating = request.form['smog_rating']

    controller.insert_vehicle(model_year, make, model, vehicle_class, engine_size, cylinder,
                              transmission, fuel_type, city_l_100km, highway_l_100km, combined_l_100km,
                              combined_mpg, co2_emission, co2_rating, smog_rating)

    return render_template('add_vehicle.html', success_message='Vehicle inserted successfully!')


@vehicle_blueprint.route('/get_all', methods=['GET'])
def get_vehicles():
    """ Handles grabbing all records from the database and rendering the index template """
    vehicles = controller.get_all_vehicles()
    return render_template('index.html', vehicles=vehicles)


@vehicle_blueprint.route('/get_one/<veh_id>', methods=['GET'])
def get_vehicle(veh_id):
    """ Handles getting a vehicle from the database and rendering an individual record """
    vehicle = controller.get_vehicle(veh_id)

    if vehicle is None:
        return render_template('index.html', error="Vehicle not found.")

    return render_template('index.html', vehicle=vehicle)


@vehicle_blueprint.route('/update_one/<veh_id>', methods=['GET'])
def update_form(veh_id):
    """ Handles updating a record and rendering the update_vehicle template """
    vehicle = controller.get_vehicle(veh_id)
    if vehicle:
        return render_template('update_vehicle.html', vehicle=vehicle)
    return redirect(url_for(('vehicle.index')))


@vehicle_blueprint.route('/update_one/<veh_id>', methods=['POST'])
def update_vehicle(veh_id):
    """ Handles updating a updating the make and model of a vehicle """
    try:
        updated_model = request.form['new_model']
        updated_make = request.form['new_make']

        updated_vehicle = {
            'make': updated_make,
            'model': updated_model
        }

        result = controller.update_vehicle(veh_id, updated_vehicle)
        vehicle = controller.get_vehicle(veh_id)
        return render_template('update_vehicle.html', vehicle=vehicle, success_message='Vehicle updated!')
    except Exception as ex:
        print(f"error: {str(ex)}")


@vehicle_blueprint.route('/delete_one/<veh_id>', methods=['POST'])
def delete_vehicle(veh_id):
    """ Handles deleting a vehicle """
    controller.delete_vehicle(veh_id)
    return redirect(url_for('vehicle.index'))


@vehicle_blueprint.route('/seed_database')
def navigate_to_seed():
    """ Handles navigating to the seed_db.html """
    return render_template('seed_db.html')


@vehicle_blueprint.route('/seed_database', methods=['POST'])
def seed_database():
    """ Handles seeding the database with new records """
    controller.seed_database()
    return render_template('seed_db.html', success_message='Database seeded successfully!')
