import obd
from utils import gps

def get_stats(connection, serial):
    try:
        rpm = int(connection.query(obd.commands.RPM).value.magnitude)
        speed = int(connection.query(obd.commands.SPEED).value.magnitude)
        temperature = int(connection.query(obd.commands.COOLANT_TEMP).value.magnitude)
        odo = int(connection.query(obd.commands.DISTANCE_SINCE_DTC_CLEAR).value.magnitude)
        location = gps.position(serial)
    except:
        rpm, speed, temperature, odo, location = 0, 0, 0, 0, gps.default

    return {
        "speed": speed,
        "rpm": rpm,
        "temp": temperature,
        "odo": odo,
        "gear": 0,
        "location": {
            "latitude": 0.0 if location is None else location['latitude'],
            "longitude": 0.0 if location is None else location['longitude']
        },
        "stressed": False
    }