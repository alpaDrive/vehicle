import pynmea2, serial, datetime

def position():
    try:
        connection = serial.Serial('/dev/ttyS0')
        while True:
            line = connection.readline().decode('latin-1')
            if line.startswith('$GPGGA'): 
                connection.close()
                data = pynmea2.parse(line)
                if data.latitude == 0.0 and data.longitude == 0.0:
                    print(f'{datetime.now().strftime("%H:%M:%S")}: Waiting for GPS signal...')
                return { 'latitude': data.latitude, 'longitude': data.longitude } 
    except:
        return { 'latitude': 0.0, 'longitude': 0.0 }

def has_fix():
    try:
        connection = serial.Serial('/dev/ttyS0')
        while True:
            line = connection.readline().decode('latin-1')
            if line.startswith('$GPGGA'):
                connection.close()
                data = pynmea2.parse(line)
                if data.latitude != 0.0 and data.longitude != 0.0:
                    return True 
                return False
    except:
        return False