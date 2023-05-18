import pynmea2

default = { 'latitude': 0.0, 'longitude': 0.0 }
def position(serial):
    try:
        line = serial.readline().decode('latin-1')  # Read a line of NMEA data and decode it
        if line.startswith('$GPGGA'):  # Example: Use GGA sentence for latitude and longitude
            return pynmea2.parse(line)
    except:
        return default