import pynmea2, serial

def position():
    try:
        connection = serial.Serial('/dev/ttyS0')
        while True:
            line = connection.readline().decode('latin-1')  # Read a line of NMEA data and decode it
            if line.startswith('$GPGGA'):  # Example: Use GGA sentence for latitude and longitude
                connection.close()
                data = pynmea2.parse(line)
                return { 'latitude': data.latitude, 'longitude': data.longitude } 
    except:
        return { 'latitude': 0.0, 'longitude': 0.0 }