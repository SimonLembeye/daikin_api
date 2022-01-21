import json
import uuid
from websocket import create_connection
import dpath.util


class DaikinAltherma:
    UserAgent = "python-daikin-altherma"

    def __init__(self, adapter_ip: str, name: str):
        self.adapter_ip = adapter_ip
        self.ws = create_connection(f"ws://{self.adapter_ip}/mca")
        self.name = name
        print(f"{name} ")

    def _requestValue(self, item: str, output_path: str, payload=None):
        reqid = uuid.uuid4().hex[0:5]
        js_request = {
            "m2m:rqp": {
                "fr": DaikinAltherma.UserAgent,
                "rqi": reqid,
                "op": 2,
                "to": f"/[0]/{item}",
            }
        }
        if payload:
            set_value_params = {
                "ty": 4,
                "op": 1,
                "pc": {
                    "m2m:cin": payload,
                },
            }
            js_request["m2m:rqp"].update(set_value_params)
        # print(f"Send to ws: {json.dumps(js_request)}")
        self.ws.send(json.dumps(js_request))
        result = json.loads(self.ws.recv())
        assert result["m2m:rsp"]["rqi"] == reqid
        assert result["m2m:rsp"]["to"] == DaikinAltherma.UserAgent
        return dpath.util.get(result, output_path)

    def _requestValueHP(self, item: str, output_path: str, payload=None):
        return self._requestValue(f"MNAE/{item}", output_path, payload)

    # ------------------------- General ----------------------------

    @property
    def adapter_model(self) -> str:
        """ Returns the model of the LAN adapter """
        # either BRP069A61 or BRP069A62
        return self._requestValue("MNCSE-node/deviceInfo", "/m2m:rsp/pc/m2m:dvi/mod")

    @property
    def error_state(self) -> bool:
        """ Returns the error state """
        return (
            self._requestValueHP("0/UnitStatus/ErrorState/la", "m2m:rsp/pc/m2m:cin/con")
            == 1
        )

    @property
    def indoor_temperature(self) -> float:
        """ Returns the indoor temperature, in °C """
        return self._requestValueHP(
            "1/Sensor/IndoorTemperature/la", "/m2m:rsp/pc/m2m:cin/con"
        )

    @property
    def outdoor_temperature(self) -> float:
        """ Returns the outdoor temperature, in °C """
        return self._requestValueHP(
            "1/Sensor/OutdoorTemperature/la", "/m2m:rsp/pc/m2m:cin/con"
        )

    # ----------------------------- Heater ------------------------------

    @property
    def power_state(self) -> bool:
        """ Returns the power state """
        return (
            self._requestValueHP("1/Operation/Power/la", "m2m:rsp/pc/m2m:cin/con")
            == "on"
        )

    @property
    def leaving_water_temperature(self) -> float:
        """ Returns the heating leaving water temperature, in °C """
        return self._requestValueHP(
            "1/Sensor/LeavingWaterTemperatureCurrent/la", "m2m:rsp/pc/m2m:cin/con"
        )

    @property
    def target_water_temperature(self) -> float:
        """ Returns the heating leaving water temperature, in °C """
        return self._requestValueHP(
            "1/Sensor/TargetLeavingWaterTemperatureCurrent/la", "m2m:rsp/pc/m2m:cin/con"
        )

    @property
    def power_consumption(self) -> dict:
        """ Returns the energy consumption in kWh per [D]ay, [W]eek, [M]onth """
        return self._requestValueHP("1/Consumption/la", "m2m:rsp/pc/m2m:cin/con")

    def set_heating(self, heating_active: bool):
        """Whether to turn the heating on(True) or off(False).
        You can confirm that it works by calling self.power_state
        """
        mode_dict = {
            True: "on",
            False: "standby",
        }
        payload = {
            "con": mode_dict[heating_active],
            "cnf": "text/plain:0",
        }
        # print(f"Output set_heating: {self._requestValueHP('1/Operation/Power', '/', payload)}")
        self._requestValueHP("1/Operation/Power", "/", payload)

    @property
    def offset_value(self) -> float:
        """ Returns the target value of tank temperature """
        return self._requestValueHP(
            "1/Operation/LeavingWaterTemperatureOffsetHeating/la",
            "m2m:rsp/pc/m2m:cin/con",
        )

    def set_offset(self, offset: float):

        payload = {
            "con": offset,
            "cnf": "text/plain:0",
        }

        self._requestValueHP(
            "1/Operation/LeavingWaterTemperatureOffsetHeating", "/", payload
        )

    # ------------------------------- Tank ---------------------------------

    @property
    def tank_power_state(self) -> bool:
        """ Returns the power state """
        return (
            self._requestValueHP("2/Operation/Power/la", "m2m:rsp/pc/m2m:cin/con")
            == "on"
        )

    @property
    def tank_powerful_state(self) -> bool:
        """ Returns the tank powerful state """
        return (
            self._requestValueHP("2/Operation/Powerful/la", "m2m:rsp/pc/m2m:cin/con")
            == 1
        )

    @property
    def tank_temperature(self) -> float:
        """ Returns the hot water tank temperature, in °C """
        return self._requestValueHP(
            "2/Sensor/TankTemperature/la", "/m2m:rsp/pc/m2m:cin/con"
        )

    @property
    def power_consumption_tank(self) -> dict:
        """ Returns the energy consumption in kWh per [D]ay, [W]eek, [M]onth """
        return self._requestValueHP("2/Consumption/la", "m2m:rsp/pc/m2m:cin/con")

    @property
    def tank_temperature_value(self) -> float:
        """ Returns the target value of tank temperature """
        return self._requestValueHP(
            "2/Operation/TargetTemperature/la", "m2m:rsp/pc/m2m:cin/con"
        )

    def set_tank_heating(self, heating_active: bool):
        """Whether to turn the heating on(True) or off(False).
        You can confirm that it works by calling self.power_state
        """
        mode_dict = {
            True: "on",
            False: "standby",
        }
        payload = {
            "con": mode_dict[heating_active],
            "cnf": "text/plain:0",
        }
        # print(f"Output set_heating: {self._requestValueHP('1/Operation/Power', '/', payload)}")
        self._requestValueHP("2/Operation/Power", "/", payload)

    def set_tank_heating_powerfull(self, powerful_active: bool):
        """Whether to turn the water tank heating powerful on(True) or off(False).
        You can confirm that it works by calling self.tank_powerful_state
        """
        mode_dict = {
            True: 1,
            False: 0,
        }

        payload = {
            "con": mode_dict[powerful_active],
            "cnf": "text/plain:0",
        }

        self._requestValueHP("2/Operation/Powerful", "/", payload)

    def set_tank_temperature(self, tank_temp: float):

        payload = {
            "con": tank_temp,
            "cnf": "text/plain:0",
        }

        self._requestValueHP("2/Operation/TargetTemperature", "/", payload)


if __name__ == "__main__":
    ad = DaikinAltherma("192.168.1.97", "Framboise")

    print("General")
    print()
    print(f"Adadter Model: {ad.adapter_model}")
    print(f"Error State: {ad.error_state}")
    print(f"Outdoor Temperature: {ad.outdoor_temperature}")
    # print(ad.indoor_temperature)
    print()

    print("Heater")
    print()
    print(f"Power State: {ad.power_state}")
    print(f"Leaving Water Temperature: {ad.leaving_water_temperature}")
    print("set heating true")
    ad.set_heating(True)
    print("set offset to 0")
    ad.set_offset(0)
    print(f"offset: {ad.offset_value}")
    print()
    print(ad.power_consumption)
    print()

    print("Tank")
    print()
    print("set tank power True")
    ad.set_tank_heating(True)
    print(f"Tank Power State : {ad.tank_power_state}")
    print("set tank heating powerfull False")
    ad.set_tank_heating_powerfull(False)
    print(f"Tank Powerfull State : {ad.tank_powerful_state}")
    print("set tank temperature to 51°C")
    ad.set_tank_temperature(50)
    print(f"Tank Temperature Target : {ad.tank_temperature_value}")
    print(f"Tank Temperature: {ad.tank_temperature}")
    print()
    print(ad.power_consumption_tank)
    print()
