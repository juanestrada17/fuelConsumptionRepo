"""
Filename: vehicle_repo_test.py
Author: Juan Estrada
Date: 2024-09-16
Description: Vehicle Repository tests for get, update and delete methods.
"""

from unittest.mock import MagicMock

import pytest
import mongomock

from repositories.vehicle_repo import VehicleRepository


@pytest.fixture(autouse=True)
def vehicle_repository():
    """ Mocks the repository and mongo db connection"""
    collection = mongomock.MongoClient().db.collection
    repository = VehicleRepository()
    repository.collection = collection
    return repository


def test_get_vehicle(vehicle_repository):
    """ Tests successfully grabbing a record from mocked database """
    vehicle_id = "f8c3de3d-1fea-4d7c-a8b0-29f63c4c3454"
    found_result = {
        'model_year': 2024,
        'make': 'Test Make',
        'model': 'Test Model',
        'vehicle_class': 'Test Vehicle Class',
        'engine_size': 1.2,
        'cylinder': 1,
        'transmission': 'Z',
        'fuel_type': 'Z',
        'city_l_100km': 22,
        'highway_l_100km': 2,
        'combined_l_100km': 2,
        'combined_mpg': 2,
        'co2_emission': 2,
        'co2_rating': 2,
        'smog_rating': 2,
        '_id': vehicle_id}

    vehicle_repository.collection.find_one = MagicMock(return_value=found_result)
    response = vehicle_repository.get_vehicle(vehicle_id)

    assert response.make == 'Test Make'
    assert response.model == 'Test Model'


def test_update_vehicle(vehicle_repository):
    """ Tests updating a vehicle """
    vehicle_id = "f8c3de3d-1fea-4d7c-a8b0-29f63c4c3454"
    updated_vehicle = {"make": "New Make", "model": "New Model"}

    updated_result = MagicMock()
    updated_result.modified_count = 1

    vehicle_repository.collection.update_one = MagicMock(return_value=updated_result)
    response = vehicle_repository.update_vehicle(vehicle_id, updated_vehicle)

    assert response.status == "200 OK"
    assert "Vehicle updated successfully" in response.get_data(as_text=True)


def test_update_vehicle_missing_model(vehicle_repository):
    """ Tests updating a vehicle with a missing model """
    vehicle_id = "f8c3de3d-1fea-4d7c-a8b0-29f63c4c3454"
    updated_vehicle = {"make": "New Make"}

    updated_result = MagicMock()
    updated_result.modified_count = 1

    vehicle_repository.collection.update_one = MagicMock(return_value=updated_result)
    response = vehicle_repository.update_vehicle(vehicle_id, updated_vehicle)

    assert response.status == "500 INTERNAL SERVER ERROR"
    assert "Error updating data: 'model'" in response.get_data(as_text=True)


def test_update_vehicle_not_found(vehicle_repository):
    """ Tests updating a vehicle not in the database """
    vehicle_id = "f8c3de3d-1fea-4d7c-a8b0-29f63c4c3454"
    updated_vehicle = {"make": "New Make", "model": "New Model"}

    updated_result = MagicMock()
    updated_result.modified_count = 0

    vehicle_repository.collection.update_one = MagicMock(return_value=updated_result)
    response = vehicle_repository.update_vehicle(vehicle_id, updated_vehicle)

    assert response.status == "404 NOT FOUND"
    assert "Vehicle not found" in response.get_data(as_text=True)


def test_delete_vehicle(vehicle_repository):
    """ Tests deleting a vehicle from the database """
    vehicle_id = "f8c3de3d-1fea-4d7c-a8b0-29f63c4c3454"
    updated_result = MagicMock()
    updated_result.deleted_count = 1

    vehicle_repository.collection.delete_one = MagicMock(return_value=updated_result)
    response = vehicle_repository.delete_vehicle(vehicle_id)
    assert response.status == "200 OK"
    assert "Vehicle deleted successfully" in response.get_data(as_text=True)
