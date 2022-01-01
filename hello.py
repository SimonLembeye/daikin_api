from flask import Flask, render_template, jsonify, make_response
from heat_pump import DaikinAltherma

framboise = DaikinAltherma("192.168.1.97", "Framboise")

app = Flask(__name__)



@app.route("/dashboard")
def index():
    return render_template("index.html", tank_temperature=framboise.tank_temperature)

@app.route("/data")
def data():
    d = {
        "name": "Framboise",
        "adapter_model": framboise.adapter_model,
        "tank_temperature": framboise.tank_temperature,
        "outdoor_temperature": framboise.outdoor_temperature,
        "leaving_water_temperature": framboise.leaving_water_temperature,
        "power_state": framboise.power_state,
        "power_consumption": framboise.power_consumption,
        "tank_power_state": framboise.tank_power_state,
        "tank_powerful_state": framboise.tank_powerful_state
    }
    return make_response(jsonify(d), 200)

@app.route("/startstop/<go>", methods=['GET'])
def startstop(go):
    if go in ["TRUE", "True", "1", "ON", "on", "true"]:
        framboise.set_heating(True)
    elif go in ["FALSE", "False", "0", "OFF", "off", "false"]:
        framboise.set_heating(False)
    else:
        return "NOOOOOON PAS bien"

    return f"Framboise are you ok ? : {framboise.power_state}"





