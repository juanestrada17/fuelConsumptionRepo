"""
Filename: route_utility.py
Author: Juan Estrada
Date: 2024-10-03
Description: Contains utility methods for the application's routes
"""

def chart_title(column):
    """ Takes a column as an argument and returns a string representing it's title"""
    match column:
        case 'make_mpg':
            return 'Combined mpg per make'
        case 'engine_mpg':
            return 'Engine size mpg scatter plot'
        case 'co2_emission':
            return 'Co2 emission histogram'
        case 'transmission':
            return 'Transmission Pie Chart'
        case 'fuel_mpg':
            return 'Combined mpg per fuel type'
        case 'consumption':
            return 'Average Fuel Consumption per make'
        case _:
            return 'Combined mpg per make'