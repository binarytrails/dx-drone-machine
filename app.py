# Vsevolod Ivanov

import json
import requests

from flask import Flask, render_template
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin

from geoip2 import database
from geoip2.errors import AddressNotFoundError

app = Flask(__name__)

CORS(app)  # This will enable CORS for all routes
#@cross_origin()  # This will enable CORS for this route
socketio = SocketIO(app, cors_allowed_origins="*") # todo enforce security to website

# Define the database location in memory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@socketio.on('connect')
def connect():
    ip = request.remote_addr
    emit('user_connected', {'ip': ip}, broadcast=True)
    print(f'Client {ip} connected.')

@socketio.on('disconnect')
def disconnect():
    ip = request.remote_addr
    print(f'Client {ip} disconnected.')


# Define the schema
class User(db.Model):
    ip_address = db.Column(db.String(40), primary_key=True)  # IPV6 address is up to 39 characters + 1 for Null termination
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, ip_address, latitude, longitude):
        self.ip_address = ip_address
        self.latitude = latitude
        self.longitude = longitude

# Create the database
with app.app_context():
    db.create_all()

# Geolocation database reader
reader = database.Reader('./databases/GeoLite2-City.mmdb')

@app.route('/geolocations')
def get_geolocations():
    # Get distinct latitudes and longitudes from the User table
    results = db.session.query(User.latitude, User.longitude).distinct().all()

    users_geoloc = []
    for result in results:
        users_geoloc.append([result.longitude, result.latitude])
        try:
            print(f"Welcome new user from {result.city}, {result.country}!")
        except:
            pass

    return {"geolocations": users_geoloc}

@app.route('/')
def index():
    ip = request.remote_addr
    # Get the geolocation data from the IP address
    try:
        response = reader.city(ip)
        latitude = response.location.latitude
        longitude = response.location.longitude
    except AddressNotFoundError:
        if ip == '127.0.0.1':
            # This is an approximation for Montreal's coordinates
            latitude = 45.5017
            longitude = -73.5673
            print(f"The IP address {ip} is not a valid GeoLocation. I presume you're in Montreal; bonjour, hi! ;)")
        else:
            print(f'The IP address {ip} is not in the database')

    # Check if user already exists
    user = User.query.get(ip)
    if not user:
        user = User(ip_address=ip, latitude=latitude, longitude=longitude)
        # Save the data into the database
        db.session.add(user)
        db.session.commit()
        print(f'Your geolocation has been stored. User IP: {user.ip_address}')
    else:
        print(f'User with IP {ip} already exists')

    # Convert the list to a JSON formatted string
    users_geoloc_json = json.dumps({"geolocations": get_geolocations()})

    # Pass the JSON string to the template
    return render_template('index.html', title="DX Drone Machine", users_geoloc=users_geoloc_json)

if __name__ == "__main__":
    #app.run(debug=True,host='0.0.0.0', port=10000)
    socketio.run(app, debug=False, host='0.0.0.0', port=10000)