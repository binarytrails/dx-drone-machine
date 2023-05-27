import requests

from flask import Flask, render_template
from flask import request   

app = Flask(__name__)

users = [{
    'ip_addr': '39.110.142.79',
    # latitude,longitude
    'geo_loc': (35.4594,139.5979)
}]

users_geoloc=[]
users_geoloc.append([-73.778137, 40.641312])
users_geoloc.append([-0.454296, 51.470020])
users_geoloc.append([116.597504, 40.072498])

@app.route("/")
def index():
    #ip_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    print("ip_addr: ", request.remote_addr)

    #response = requests.get(
    #    "https://geolocation-db.com/json/{ip_addr}&position=true".format(ip_addr='39.110.142.79'),
    #    timeout=10
    #).json()
    # users.append({'ip_addr': request.remote_addr, 'geo_loc': (response['latitude'],response['longitude'])})

    return render_template("index.html", title="DX Drone Machine", users_geoloc=users_geoloc)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=10000)