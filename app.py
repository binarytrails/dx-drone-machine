from flask import Flask, render_template
from flask import request   

app = Flask(__name__)

users_geoloc=[]
users_geoloc.append([-73.778137, 40.641312])
users_geoloc.append([-0.454296, 51.470020])
users_geoloc.append([116.597504, 40.072498])

@app.route("/")
def index():
    #ip_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    print("ip_addr: ", request.remote_addr)
    return render_template("index.html", title="DX Drone Machine", users_geoloc=users_geoloc)
