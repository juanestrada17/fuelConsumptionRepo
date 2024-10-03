"""
Filename: datasetReaderTest.py
Author: Juan Estrada
Date: 2024-09-16
Description: Tests the datasetReader() function
"""

from unittest.mock import patch
import pandas as pd
from DataSetReader import dataset_reader


@patch('DataSetReader.pd.read_csv')
def test_dataset_read(mock_read_csv):
    """ Tests the datasetReader by mocking the csv"""
    mock_df = pd.DataFrame({
        'Model year': [2024],
        'Make': ['Test Make'],
        'Model': ['Test Model'],
        'Vehicle class': ['Sports'],
        'Engine size (L)': [1.5],
        'Cylinders': [1],
        'Transmission': ['Test trans'],
        'Fuel type': ['Test Fuel'],
        'City (L/100 km)': [8.5],
        'Highway (L/100 km)': [1.2],
        'Combined (L/100 km)': [23],
        'Combined (mpg)': [123],
        'CO2 emissions (g/km)': [32],
        'CO2 rating': [6],
        'Smog rating': [7]
    })

    mock_read_csv.return_value = mock_df

    vehicles = dataset_reader("test_csv")
    assert len(vehicles) == 1
    assert vehicles[0].vehicle_class == 'Sports'
    assert vehicles[0].smog_rating == 7
    assert vehicles[0].model == 'Test Model'


@patch('DataSetReader.pd.read_csv', side_effect=FileNotFoundError)
def test_dataset_reader_file_not_found(mock_read_csv):
    """ Tests the FileNotFoundError exception to the dataSetReader"""
    vehicles = dataset_reader("notFound.csv")

    assert len(vehicles) == 0


@patch('DataSetReader.pd.read_csv')
def test_dataset_read_none_values(mock_read_csv):
    """ Tests the dataSetReader when inserting elements without the correct type """
    mock_df = pd.DataFrame({
        'Model year': [2024],
        'Make': ['Test Make'],
        'Model': None,
        'Vehicle class': None,
        'Engine size (L)': [1.5],
        'Cylinders': [1],
        'Transmission': ['Test trans'],
        'Fuel type': ['Test Fuel'],
        'City (L/100 km)': [8.5],
        'Highway (L/100 km)': [23],
        'Combined (L/100 km)': [23],
        'Combined (mpg)': [123],
        'CO2 emissions (g/km)': [32],
        'CO2 rating': [6],
        'Smog rating': None
    })

    mock_read_csv.return_value = mock_df

    vehicles = dataset_reader("test_csv")
    assert len(vehicles) == 1
    assert vehicles[0].vehicle_class is None
    assert vehicles[0].smog_rating is None
    assert vehicles[0].model is None

