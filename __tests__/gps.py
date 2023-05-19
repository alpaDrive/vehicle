import serial
import pynmea2
from time import sleep

while True:
    connection = serial.Serial("/dev/ttyS0")
    try:
        line = connection.readline().decode('latin-1')  # Read a line of NMEA data and decode it
        if line.startswith('$GPGGA'):  # Example: Use GGA sentence for latitude and longitude
            data = pynmea2.parse(line)
            print("Latitude:", data.latitude)
            print("Longitude:", data.longitude)
        connection.close()
    except Exception as e:
        print(f'An exception occured {e}')
        print('Retrying...')