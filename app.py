"""
Filename: app.py
Author: Juan Estrada
Date: 2024-09-16
Description: Registers the routes and starts the Flask application
"""

from flask import Flask
from routes.vehicle_routes import vehicle_blueprint
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)
app.register_blueprint(vehicle_blueprint)


if __name__ == '__main__':
    app.run(debug=True)