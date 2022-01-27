import sqlite3
from heat_pump import DaikinAltherma

connection = sqlite3.connect("database.db")
framboise = DaikinAltherma("192.168.1.97", "Framboise")

cur = connection.cursor()

current_data = {
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

cur.execute(
    "INSERT INTO measurements (outdoor_temperature, heater_power_state) VALUES (?, ?)",
    (current_data["outdoor_temperature"], current_data["heater_power_state"]),
)


connection.commit()
connection.close()
