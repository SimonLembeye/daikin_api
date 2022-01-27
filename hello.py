from flask import Flask, render_template, jsonify, make_response
from heat_pump import DaikinAltherma
from helpers_db import query_db
import json

framboise = DaikinAltherma("192.168.1.97", "Framboise")

app = Flask(__name__, static_folder='static', template_folder="templates")


app = Flask(__name__)


@app.route("/dashboard")
def index():
    return render_template(
        "index.html",
        tank_temperature=framboise.tank_temperature,
        tank_temperature_target=framboise.tank_temperature_value,
        tank_power_state=framboise.tank_power_state,
        tank_powerful_state=framboise.tank_powerful_state,
        leaving_water_temperature=framboise.leaving_water_temperature,
        offset_leaving_temperature=framboise.offset_value,
        heater_power_state=framboise.power_state,
        error_state=framboise.error_state,
        outdoor_temperature=framboise.outdoor_temperature,
        adapter_model=framboise.adapter_model,
    )


@app.route("/data")
def data():
    d = {
        "name": "Framboise",
        "adapter_model": framboise.adapter_model,
        "outdoor_temperature": framboise.outdoor_temperature,
        "error_state": framboise.error_state,
        "heater_power_state": framboise.power_state,
        "leaving_water_temperature": framboise.leaving_water_temperature,
        "offset_leaving_temperature": framboise.offset_value,
        "heater_power_consumption": framboise.power_consumption,
        "tank_power_state": framboise.tank_power_state,
        "tank_powerful_state": framboise.tank_powerful_state,
        "tank_temperature_target": framboise.tank_temperature_value,
        "tank_temperature": framboise.tank_temperature,
        "tank_power_consumption": framboise.power_consumption_tank,
    }
    return make_response(jsonify(d), 200)


@app.route("/read_database")
def read_database():
    my_query = query_db("select * from measurements")
    json_output = json.dumps(my_query)
    return make_response(json_output, 200)


@app.route("/startstopheater/<go>", methods=["GET"])
def startstopheater(go):
    if go in ["TRUE", "True", "1", "ON", "on", "true"]:
        framboise.set_heating(True)
    elif go in ["FALSE", "False", "0", "OFF", "off", "false", "stanby", "Standby"]:
        framboise.set_heating(False)
    else:
        return "NOOOOOON PAS bien"

    return f"Framboise are you ok ? : {framboise.power_state}"


@app.route("/startstoptank/<go>", methods=["GET"])
def startstoptank(go):
    if go in ["TRUE", "True", "1", "ON", "on", "true"]:
        framboise.set_tank_heating(True)
    elif go in ["FALSE", "False", "0", "OFF", "off", "false", "stanby", "Standby"]:
        framboise.set_tank_heating(False)
    else:
        return "NOOOOOON PAS bien"

    return f"Framboise tank are you ok ? : {framboise.tank_power_state}"


@app.route("/startstoptankpowerfull/<go>", methods=["GET"])
def startstoptankpowerfull(go):
    if go in ["TRUE", "True", "1", "ON", "on", "true"]:
        framboise.set_tank_heating_powerfull(True)
    elif go in ["FALSE", "False", "0", "OFF", "off", "false", "stanby", "Standby"]:
        framboise.set_tank_heating_powerfull(False)
    else:
        return "NOOOOOON PAS bien"

    return f"Framboise tank are you powerfull ? : {framboise.tank_powerful_state}"


@app.route("/offset/<value>", methods=["GET"])
def set_offset(value):
    val = float(value)
    framboise.set_offset(val)
    return f"Offset : {value}"


@app.route("/tanktemperature/<temperature>", methods=["GET"])
def set_tank_temperature(temperature):
    val = float(temperature)
    framboise.set_tank_temperature(val)
    return f"Tank Temperature Target : {temperature}"
