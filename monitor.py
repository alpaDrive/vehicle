import obd, serial, pynmea2, json

class GPS:
    def __init__(self):
        self.connection = serial.Serial("/dev/ttyS0")

    def position(self):
        try:
            line = self.connection.readline().decode('latin-1')
            if line.startswith('$GPGGA'):
                return pynmea2.parse(line)
        except:
            return { "latitude": 0.0, "longitude": 0.0 }

class OBDInterface:
    def __init__(self, vehicle_id, message_sender):
        self.vehicle_id = vehicle_id
        self.message_sender = message_sender
        self.connection = obd.OBD('/dev/ttyUSB0')
        self.gps = GPS()
        self.stats = {
            "speed": None,
            "rpm": None,
            "temp": None,
            "gear": 0,
            "stressed": False
        }

    async def start(self):

        while True:
            # Get current values
            rpm = self.parse_response(self.connection.query(obd.commands.RPM).value) # try with .magnitude
            speed = self.parse_response(self.connection.query(obd.commands.SPEED).value)
            temperature = self.parse_response(self.connection.query(obd.commands.COOLANT_TEMP).value)
            odo = self.parse_response(self.connection.query(obd.commands.DISTANCE_SINCE_DTC_CLEAR).value)
            gear = self.estimate_gear_position(rpm, speed)
            location = self.gps.position()

            self.stats = {
                "speed": speed,
                "rpm": rpm,
                "temp": temperature,
                "odo": odo,
                "gear": gear,
                "location": {
                    "latitude": location.latitude,
                    "longitude": location.longitude
                },
                "stressed": self.is_vehicle_under_stress(rpm, speed, gear)
            }

            self.message_sender.send_message(json.dumps(self.stats))
    
    def parse_response(self, response):
        return float(str(response).split(" ")[0])

    def is_vehicle_under_stress(self, rpm, speed, gear_position):
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

    def estimate_gear_position(self, engine_rpm, speedometer_reading):
        # Set up the gear ratios for the 2015 Maruti Suzuki Swift Dzire
        gear_ratios = {
            '1st gear': 3.545,
            '2nd gear': 1.904,
            '3rd gear': 1.233,
            '4th gear': 0.911,
            '5th gear': 0.725
        }
        
        # Calculate the ratio of engine RPM to speedometer reading
        ratio = engine_rpm / speedometer_reading
        
        # Set up the fuzzy logic rules
        rules = {
            '1st or 2nd gear': {'min': 0.0, 'max': 0.6},
            '3rd gear': {'min': 0.6, 'max': 1.1},
            '4th gear': {'min': 1.1, 'max': 1.4},
            '5th gear': {'min': 1.4, 'max': 2.0}
        }
        
        # Apply the rules to estimate the gear position
        gear_position = None
        for gear, values in rules.items():
            if values['min'] <= ratio <= values['max']:
                gear_position = gear
                break
        
        # If no gear position was estimated, use the highest or lowest gear as a fallback
        if gear_position is None:
            if ratio < rules['1st or 2nd gear']['min']:
                gear_position = '1st or 2nd gear'
            elif ratio > rules['5th gear']['max']:
                gear_position = '5th gear'
        
        # Look up the gear ratio for the estimated gear position
        if gear_position is not None:
            for gear, ratio in gear_ratios.items():
                if gear_position in gear:
                    return int(gear[0])
        
        # If no gear position could be estimated, assume neutral
        return 0
    
    def get_rpm(self):
        return self.connection.query(obd.commands.RPM).value

    def get_speed(self):
        return self.connection.query(obd.commands.SPEED).value
