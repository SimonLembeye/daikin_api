from flask import Flask, render_template, jsonify, make_response
from heat_pump import DaikinAltherma

framboise = DaikinAltherma("192.168.1.97", "Framboise")

app = Flask(__name__)



@app.route("/dashboard")
def index():
    return render_template("index.html", tank_temperature=framboise.tank_temperature, )

@app.route("/data")
def data():
    d = {
        "name": "Framboise",
        "tank_temperature": framboise.tank_temperature,
    }
    return d




