DROP TABLE IF EXISTS measurements;

CREATE TABLE measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    outdoor_temperature FLOAT NOT NULL,
    heater_power_state BOOLEAN NOT NULL
);