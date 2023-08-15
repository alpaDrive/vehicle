import obd
from utils import gps

def predict_gear(speed, rpm):
    lookup_table = {
        (0, 10): {
            (900, 1100): 1,
            (0, 900): 0
        },
        (10, 20): {
            (1000, 2000): 1,
            (900, 1000): 2,
            (0, 900): 0
        },
        (20, 30): {
            (2000, 4000): 1,
            (1100, 2000): 2,
            (900, 1100): 3,
            (0, 900): 0
        },
        (30, 40): {
            (5000, 8000): 1,
            (2000, 5000): 2,
            (1200, 2000): 3,
            (900, 1200): 4,
            (0, 900): 0
        },
        (40, 50): {
            (5000, 8000): 1,
            (2500, 5000): 2,
            (1500, 2500): 3,
            (1100, 1500): 4,
            (0, 1000): 0
        },
        (50, 60): {
            (6000, 8000): 1,
            (4000, 6000): 2,
            (2500, 4000): 3,
            (1500, 2500): 4,
            (1000, 1500): 5,
            (0, 1000): 0
        },
        (60, 80): {
            (6500, 8000): 1,
            (5000, 6500): 2,
            (3500, 5000): 3,
            (2500, 3500): 4,
            (1000, 2500): 5,
            (0, 1000): 0
        },
        (80, 100): {
            (7000, 8000): 1,
            (6000, 7000): 2,
            (5000, 6000): 3,
            (3000, 5000): 4,
            (1301, 3000): 5,
            (0, 1300): 0
        },
        (100, 121): {
            (8000, 9000): 1,
            (6000, 8000): 2,
            (5000, 6000): 3,
            (4000, 5000): 4,
            (1100, 4000): 5,
            (0, 1100): 0
        }
    }

    # Iterate through the lookup table and find the matching gear for the given RPM and speed
    for (min_speed, max_speed), rpm_table in lookup_table.items():
        if speed in range(min_speed, max_speed):
            for (min_rpm, max_rpm), gear in rpm_table.items():
                if rpm in range(min_rpm, max_rpm):
                    return gear

    return 0 # assume neutral if nothing fits

def is_vehicle_under_stress(rpm, speed, gear_position):
    try:
        # Define threshold values for RPM, speed, and gear position
        MAX_RPM = 6000
        MAX_SPEED = 80

        # Check if the RPM is above the maximum threshold for the current gear
        max_rpm_for_gear = gear_position * 1000  # Assuming each gear has a 1000 RPM range
        if rpm > max_rpm_for_gear:
            return True

        # Check if the speed is below the minimum threshold for the current gear
        min_speed_for_gear = gear_position * 10  # Assuming each gear has a 10 km/h range
        if speed < min_speed_for_gear:
            return True

        # If none of the above conditions are met, return False
        return False
    except:
        return False

def get_stat(connection, command):
    try:
        return int(connection.query(command).value.magnitude)
    except:
        return 0

def get_stats(connection):
    rpm = get_stat(connection, obd.commands.RPM)
    speed = get_stat(connection, obd.commands.SPEED)
    temperature = get_stat(connection, obd.commands.COOLANT_TEMP)
    odo = get_stat(connection, obd.commands.DISTANCE_SINCE_DTC_CLEAR)
    fuel = get_stat(connection, obd.commands.FUEL_LEVEL)
    gear = predict_gear(speed, rpm)
    location = gps.position()

    return {
        "speed": speed,
        "rpm": rpm,
        "temp": temperature,
        "odo": odo,
        "gear": gear,
        "fuel": fuel,
        "location": {
            "latitude": location['latitude'],
            "longitude": location['longitude']
        },
        "stressed": False # we would call is_vehicle_under_stress() here, but in this version, it's not yet working
    }